import json
import time
from pathlib import Path

from utils.logger import logger
from src.openai.client import OpenAIClient

PRE_SCORING_PROMPT_PATH = Path(
    "prompts/stages/2-assessement/pre-scoring-assessement-prompt.md"
)
SCORING_PROMPT_PATH = Path("prompts/stages/2-assessement/scoring-assessement-prompt.md")
GENERAL_COMMENT_PROMPT_PATH = Path("prompts/stages/5-final-comments/general-comment.md")


class Assessment:
    """
    This class is responsible for assessing the candidate's solution.
    """

    def __init__(
        self,
        task: str,
        pre_scoring_prompt_path: Path = PRE_SCORING_PROMPT_PATH,
        scoring_prompt_path: Path = SCORING_PROMPT_PATH,
        general_comment_prompt_path: Path = GENERAL_COMMENT_PROMPT_PATH,
    ):
        self.criterions = [
            "content",
            "communicative-achievement",
            "organisation",
            "language",
        ]

        self.task = task

        with open(pre_scoring_prompt_path, "r", encoding="utf-8") as file:
            self.pre_scoring_assessment_prompt = file.read()

        with open(scoring_prompt_path, "r", encoding="utf-8") as file:
            self.scoring_assessment_prompt = file.read()

        with open(general_comment_prompt_path, "r", encoding="utf-8") as file:
            self.general_comment_prompt = file.read()

        logger.info("Initialized Assessement")

    def pre_scoring_assessment(
        self,
        task_understanding: str,
        candidate_solution: str,
        openai_client: OpenAIClient,
    ) -> dict[str, str]:
        """
        Before scoring the assessment, we need to get a detailed analysis of
        the candidate's performance on each criterion.

        This function will return a dictionary of criterion names as keys and
        analysis as values.
        """

        pre_scoring_prompt = self.pre_scoring_assessment_prompt

        analysis = {}
        for criterion in self.criterions:
            criterion_prompt = pre_scoring_prompt.replace("{Criterion}", criterion)

            criterion_definition_path = Path(
                f"prompts/stages/2-assessement/{criterion}/definition.md"
            )

            with open(criterion_definition_path, "r", encoding="utf-8") as file:
                criterion_definition = file.read()

            criterion_prompt = criterion_prompt.replace(
                "{Criterion-definition}",
                criterion_definition,
            )

            criterion_prompt = criterion_prompt.replace(
                "{Task}",
                self.task,
            )

            criterion_prompt = criterion_prompt.replace(
                "{Task-Understanding}",
                task_understanding,
            )

            criterion_prompt = criterion_prompt.replace(
                "{Candidates-Solution}",
                candidate_solution,
            )

            response = openai_client.get_response(
                criterion_prompt, response_format={"type": "json_object"}
            )

            response_dict = json.loads(response)
            analysis[criterion] = response_dict.get("analysis", "No analysis found")

        return analysis

    def get_criterion_scores(
        self,
        analysis: dict[str, str],
        task_description: str,
        openai_client: OpenAIClient,
        model: str = "gpt-4.1",
    ) -> dict[str, tuple[int, str]]:
        """
        Get the score for a specific criterion.

        This function will return a dictionary of criterion names as keys and
        scores and justifications as values.

        The idea behind this is that an LLM can infer a score for an analysis of a
        certain criterion. For this we do not need to provide the tasks context since
        the score should be based on the analysis alone.
        """

        scoring_prompt = self.scoring_assessment_prompt
        scoring_prompt = scoring_prompt.replace("{Task-Description}", task_description)

        scores = {}
        for criterion, criterion_analysis in analysis.items():
            logger.info(f"Starting scoring process for criterion: {criterion}")

            criterion_descriptor_path = Path(
                f"prompts/stages/2-assessement/{criterion}/descriptor.md"
            )

            with open(criterion_descriptor_path, "r", encoding="utf-8") as file:
                criterion_descriptor = file.read()
                logger.debug(
                    f"Loaded descriptor for {criterion} ({len(criterion_descriptor)} chars)"
                )

            criterion_scoring_prompt = scoring_prompt.replace(
                "{Criterion-descriptor}",
                criterion_descriptor,
            )

            criterion_scoring_prompt = criterion_scoring_prompt.replace(
                "{Criterion}", criterion
            )

            criterion_scoring_prompt = criterion_scoring_prompt.replace(
                "{Analysis}", criterion_analysis
            )

            logger.debug(
                f"Constructed scoring prompt for {criterion} ({len(criterion_scoring_prompt)} chars)"
            )
            logger.info(f"Requesting score evaluation for '{criterion}' criterion")

            response = openai_client.get_response(
                criterion_scoring_prompt,
                response_format={"type": "json_object"},
                model=model,
            )

            response_dict = json.loads(response)
            score = response_dict.get("score", 0)
            justification = response_dict.get("justification", "No justification found")

            logger.info(f"Received score for {criterion}: {score}/5")
            logger.debug(
                f"Justification length for {criterion}: {len(justification)} chars"
            )

            scores[criterion] = (score, justification)
            time.sleep(1)

        return scores

    def get_general_comment(
        self,
        task_understanding: str,
        candidate_solution: str,
        criterion_scores: dict[str, tuple[int, str]],
        openai_client: OpenAIClient,
    ) -> str:
        """
        Get the general comment for the candidate's solution based on the
        criterion scores.
        """

        general_comment_prompt = self.general_comment_prompt

        general_comment_prompt = general_comment_prompt.replace(
            "{Task}",
            self.task,
        )

        general_comment_prompt = general_comment_prompt.replace(
            "{Candidates-Solution}",
            candidate_solution,
        )

        general_comment_prompt = general_comment_prompt.replace(
            "{Task-Understanding}",
            task_understanding,
        )

        general_comment_prompt = general_comment_prompt.replace(
            "{Criterion-Scores}",
            json.dumps(criterion_scores),
        )

        response = openai_client.get_response(
            general_comment_prompt, response_format={"type": "json_object"}
        )

        response_dict = json.loads(response)
        return response_dict.get("general_comment", "No general comment found")

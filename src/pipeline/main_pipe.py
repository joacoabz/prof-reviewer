import json
from pathlib import Path
from src.ocr.ocr import OCR
from src.openai.client import OpenAIClient
from src.pipeline.assessement import Assessment
from utils.logger import PipelineLogger, log_time


TASK_UNDERSTANDING_PROMPT_PATH = Path(
    "prompts/stages/1-task-understanding/task-understanding.md"
)
DETAILED_ANALYSIS_PROMPT_PATH = Path(
    "prompts/stages/4-detailed-analysis/detailed-analysis.md"
)


class Pipeline:
    def __init__(
        self,
        task: str,
        task_understanding_prompt_path: Path = TASK_UNDERSTANDING_PROMPT_PATH,
        detailed_analysis_prompt_path: Path = DETAILED_ANALYSIS_PROMPT_PATH,
    ):
        self.task = task
        self.pipeline_logger = PipelineLogger(task)

        with open(task_understanding_prompt_path, "r", encoding="utf-8") as file:
            self.task_understanding_prompt = file.read()

        with open(detailed_analysis_prompt_path, "r", encoding="utf-8") as file:
            self.detailed_analysis_prompt = file.read()

    def task_understanding(self, task: str, openai_client: OpenAIClient) -> str:
        """
        The purpose of this step of the pipeline is to have a detailed understanding
        of the task. This is to be able to assess the student's solution in the
        context of the task.

        Args:
            task: The task to be assessed.

        Returns:
            A string representing the detailed understanding of the task.
        """
        with self.pipeline_logger.step_timing("task_understanding"):
            task_understanding_prompt = self.task_understanding_prompt.replace(
                "{Task}", task
            )

            response = openai_client.get_response(
                task_understanding_prompt, response_format={"type": "json_object"}
            )

            response_dict = json.loads(response)
            task_understanding = response_dict.get(
                "task_understanding", "No task understanding found"
            )

            return task_understanding

    def assessment(
        self,
        task_understanding: str,
        students_solution: str,
        openai_client: OpenAIClient,
    ) -> tuple[str, dict[str, tuple[int, str]], dict[str, str]]:
        """
        The purpose of this step of the pipeline is to assess the student's solution
        in the context of the task.

        The assessement works in a two-step fashion:

        1. Make a thourough analysis on the student's solution for each criterion.
        2. Using the analysis, make a comparison between the student's solution
        and the criterion descriptors from the Cambridge English Scale in order
        to determine the score for each criterion.

        Args:
            overview: The overview of the student's solution.
            task_understanding: The detailed understanding of the task.
            students_solution: The student's solution to the task.

        Returns:
            A general comment on the student's solution.
            A dictionary with the score for each criterion.
            A dictionary with the analysis for each criterion.
        """
        assessment = Assessment(task=self.task)

        with self.pipeline_logger.step_timing("analysis"):
            analysis = assessment.pre_scoring_assessment(
                task_understanding=task_understanding,
                candidate_solution=students_solution,
                openai_client=openai_client,
            )
            self.pipeline_logger.log_analysis(analysis)

        with self.pipeline_logger.step_timing("criterion_scoring"):
            criterion_scores = assessment.get_criterion_scores(
                analysis=analysis,
                task_understanding=task_understanding,
                candidate_solution=students_solution,
                openai_client=openai_client,
            )
            self.pipeline_logger.log_criterion_scores(criterion_scores)

        with self.pipeline_logger.step_timing("general_comment"):
            general_comment = assessment.get_general_comment(
                task_understanding=task_understanding,
                candidate_solution=students_solution,
                criterion_scores=criterion_scores,
                openai_client=openai_client,
            )
            self.pipeline_logger.log_general_comment(general_comment)

        return general_comment, criterion_scores, analysis

    def detailed_analysis(
        self,
        task_understanding: str,
        students_solution: str,
        analysis: str,
        openai_client: OpenAIClient,
    ) -> list[dict[str, str]]:
        """
        The purpose of this step of the pipeline is to make a detailed analysis
        of the student's solution.
        """
        with self.pipeline_logger.step_timing("detailed_analysis"):
            detailed_analysis_prompt = self.detailed_analysis_prompt.replace(
                "{Task}", self.task
            )

            detailed_analysis_prompt = detailed_analysis_prompt.replace(
                "{Task-Undestanding}", task_understanding
            )

            detailed_analysis_prompt = detailed_analysis_prompt.replace(
                "{Candidates-Solution}", students_solution
            )

            detailed_analysis_prompt = detailed_analysis_prompt.replace(
                "{Analysis}", analysis
            )

            response = openai_client.get_response(
                detailed_analysis_prompt, response_format={"type": "json_object"}
            )

            response_dict = json.loads(response)
            detailed_analysis = response_dict.get(
                "improvement_areas", "No detailed analysis found"
            )

            self.pipeline_logger.log_detailed_analysis(detailed_analysis)

            return detailed_analysis

    def understand_solution(
        self,
        image_paths: list[Path],
        openai_client: OpenAIClient,
    ) -> str:
        """
        The purpose of this step of the pipeline is to understand the image
        that the student has uploaded.

        Args:
            prompt: The prompt to be used to understand the image.
        """
        with self.pipeline_logger.step_timing("understand_solution"):
            ocr = OCR(openai_client=openai_client)
            solution = ocr.extract_text(image_paths=image_paths)
            return solution

    def run(
        self,
        image_paths: list[Path],
    ) -> tuple[str, dict[str, tuple[int, str]], list[dict[str, str]]]:
        """
        Execute the complete assessment pipeline.

        This method orchestrates the entire assessment process by:
        1. Converting the student's image to text
        2. Creating an overview of the solution
        3. Developing a detailed understanding of the task
        4. Performing the assessment based on Cambridge English criteria

        Returns:
            - str: A general comment on the student's solution
            - dict[str, tuple[int, str]]: A dictionary mapping criterion names to
                tuples of (score, justification)
        """
        with log_time("Complete pipeline execution"):
            try:
                openai_client = OpenAIClient()

                students_solution = self.understand_solution(
                    image_paths=image_paths, openai_client=openai_client
                )
                self.pipeline_logger.log_student_solution(students_solution)

                task_understanding_obj = self.task_understanding(
                    task=self.task, openai_client=openai_client
                )
                task_understanding = json.dumps(task_understanding_obj)
                self.pipeline_logger.log_task_understanding(task_understanding_obj)

                general_comment, criterion_scores, analysis = self.assessment(
                    task_understanding=task_understanding,
                    students_solution=students_solution,
                    openai_client=openai_client,
                )

                analysis = json.dumps(analysis)

                detailed_analysis = self.detailed_analysis(
                    task_understanding=task_understanding,
                    students_solution=students_solution,
                    analysis=analysis,
                    openai_client=openai_client,
                )

                self.pipeline_logger.complete_run()

                return general_comment, criterion_scores, detailed_analysis
            except Exception as e:
                raise e

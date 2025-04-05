import sys
import time
import json
import os
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Tuple

from loguru import logger


def setup_logger(log_level: str = "INFO"):
    """
    Configure and set up the logger with console handler only.

    Args:
        log_level: Minimum log level to capture

    Returns:
        The configured logger instance
    """
    # Remove default handlers
    logger.remove()

    # Add console handler with colors
    logger.add(
        sys.stderr,
        level=log_level,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level}</level> | "
            "<cyan>{file.name}:{function}:{line}</cyan> - "
            "<level>{message}</level>"
        ),
        colorize=True,
    )

    return logger


@contextmanager
def log_time(task_name: str, level: str = "INFO"):
    """
    Context manager to log the execution time of a code block.

    Args:
        task_name: Name of the task being timed
        level: Log level to use

    Example:
        with log_time("Data processing"):
            process_data()
    """
    start_time = time.time()
    logger.log(level, f"Starting {task_name}...")
    try:
        yield
    finally:
        elapsed = time.time() - start_time
        logger.log(level, f"Completed {task_name} in {elapsed:.2f} seconds")


class PipelineLogger:
    """
    Logger class for pipeline runs that handles structured logging to a single file.
    """

    def __init__(self, task: str):
        self.run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_dir = Path("logs")
        self.log_file = self.log_dir / f"pipeline_run_{self.run_id}.json"
        self.pipeline_data = {
            "run_id": self.run_id,
            "task": task,
            "timestamp": datetime.now().isoformat(),
            "students_solution": "",
            "task_understanding": "",
            "analysis": {},
            "criterion_scores": {},
            "general_comment": "",
        }

        # Create logs directory if it doesn't exist
        os.makedirs(self.log_dir, exist_ok=True)

        logger.info(f"Initialized Pipeline Logger with run_id: {self.run_id}")
        self.save()

    def save(self):
        """Save the current pipeline data to the log file."""
        # Convert tuple values in criterion_scores to dictionaries for JSON serialization
        json_data = self.pipeline_data.copy()
        if "criterion_scores" in json_data and json_data["criterion_scores"]:
            json_data["criterion_scores"] = {
                criterion: {"score": score, "justification": justification}
                for criterion, (score, justification) in json_data[
                    "criterion_scores"
                ].items()
            }

        with open(self.log_file, "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=4)
        logger.debug(f"Pipeline data saved to {self.log_file}")

    def log_student_solution(self, solution: str):
        """Log the student's solution."""
        self.pipeline_data["students_solution"] = solution
        logger.info("Student solution extracted and logged")
        self.save()

    def log_task_understanding(self, understanding: Any):
        """Log the task understanding."""
        self.pipeline_data["task_understanding"] = understanding
        logger.info("Task understanding completed and logged")
        self.save()

    def log_analysis(self, analysis: Dict[str, str]):
        """Log the analysis results."""
        self.pipeline_data["analysis"] = analysis
        logger.info("Pre-scoring analysis completed and logged")
        self.save()

    def log_criterion_scores(self, scores: Dict[str, Tuple[int, str]]):
        """Log the criterion scores."""
        self.pipeline_data["criterion_scores"] = scores
        logger.info("Criterion scoring completed and logged")
        self.save()

    def log_general_comment(self, comment: str):
        """Log the general comment."""
        self.pipeline_data["general_comment"] = comment
        logger.info("General comment generated and logged")
        self.save()

    def complete_run(self):
        """Mark the pipeline run as completed."""
        self.pipeline_data["completed"] = True
        self.pipeline_data["completion_time"] = datetime.now().isoformat()
        self.save()
        logger.info(f"Pipeline run {self.run_id} completed. Log file: {self.log_file}")

    @contextmanager
    def step_timing(self, step_name: str):
        """Context manager to time and log a pipeline step."""
        logger.info(f"Starting pipeline step: {step_name}")
        start_time = time.time()
        try:
            yield
        finally:
            elapsed = time.time() - start_time
            self.pipeline_data.setdefault("step_timings", {})[step_name] = elapsed
            logger.info(
                f"Completed pipeline step: {step_name} in {elapsed:.2f} seconds"
            )
            self.save()


logger = setup_logger()  # noqa F811

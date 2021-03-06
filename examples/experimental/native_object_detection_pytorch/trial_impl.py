import argparse
import json
import pathlib

from determined import experimental
import determined as det
import model_def

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        dest="config",
        help="Specifies Determined Experiment configuration.",
        default="{}",
    )
    parser.add_argument(
        "--mode", dest="mode", help="Specifies local or cluster mode.", default="cluster"
    )
    args = parser.parse_args()

    dataset_url = (
        "https://determined-ai-public-datasets.s3-us-west-2.amazonaws.com/"
        "PennFudanPed/PennFudanPed.zip"
    )
    config = {
        "data": {"url": dataset_url},
        "hyperparameters": {
            "learning_rate": det.Constant(value=0.005),
            "momentum": det.Constant(value=0.9),
            "weight_decay": det.Constant(value=0.0005),
            "global_batch_size": det.Constant(value=2),
        },
        "batches_per_step": 1,
        "searcher": {
            "name": "single",
            "metric": "val_avg_iou",
            "max_steps": 16,
            "smaller_is_better": False,
        },
    }
    config.update(json.loads(args.config))

    experimental.create(
        trial_def=model_def.ObjectDetectionTrial,
        config=config,
        mode=experimental.Mode(args.mode),
        context_dir=str(pathlib.Path.cwd()),
    )

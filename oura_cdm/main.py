from oura_cdm.pipeline import run, validate_run, write_artifacts
from oura_cdm.parse_cli import get_pipeline_inputs


if __name__ == "__main__":
    inputs = get_pipeline_inputs()
    artifacts = run(**inputs)
    validate_run(artifacts)
    write_artifacts(artifacts, inputs['target_folder_name'])



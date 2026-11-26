"""预测实验 Runner 占位。"""


class ExperimentRunner:
    def run(self, dataset_name: str, method_name: str, config: dict) -> str:
        # TODO: load dataset, call method.predict, persist each raw prediction,
        # capture run metadata, support failures and resume.
        raise NotImplementedError("TODO: implement experiment runner")

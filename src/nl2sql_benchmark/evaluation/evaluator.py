"""统一评估入口占位。"""


class Evaluator:
    def evaluate_run(self, run_dir: str) -> dict:
        # TODO: load predictions + Gold data, execute SQL, compute metrics, write reports.
        # TODO: evaluation must never invoke the NL2SQL method again.
        raise NotImplementedError("TODO: implement unified evaluation")

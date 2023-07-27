import pathlib
from dataclasses import dataclass

import pandas as pd

CURRENT_DIR = pathlib.Path(__file__).parent.resolve()

USERS_FILE = "users.csv"
USER_EXPERIMENTS_FILE = "user_experiments.csv"
COMPOUNDS_FILE = "compounds.csv"


@dataclass
class SeedData:
    users_seed = None
    user_experiments_seed = None
    compounds_seed = None

    def __post_init__(self):
        self.load_users()
        self.load_user_experiments()
        self.load_compounds()

    @staticmethod
    def _as_list_of_tuples(df: pd.DataFrame):
        """Transforms row values from a dataframe into a list of tuples for
        each row.
        """
        return [tuple(row) for row in df.values]

    @property
    def experiment_compounds(self):
        df = self.user_experiments_seed
        # New line for multiple compound ids
        df = df.assign(
            experiment_compound_ids=df["experiment_compound_ids"].str.split(";")
        ).explode("experiment_compound_ids")
        df["experiment_compound_ids"] = df["experiment_compound_ids"].astype(
            int
        )
        df = df[["experiment_id", "experiment_compound_ids"]]
        return self._as_list_of_tuples(df)

    @property
    def experiment(self):
        df = self.user_experiments_seed[
            ["experiment_id", "user_id", "experiment_run_time"]
        ]
        return self._as_list_of_tuples(df)

    def load_users(self):
        """Imports user data from a csv."""
        df = pd.read_csv(
            f"{CURRENT_DIR}/{USERS_FILE}",
            names=[
                "user_id",
                "name",
                "email",
                "signup_date",
            ],
            skiprows=2,
            sep="\t",
        )
        # Clean
        df["user_id"] = df["user_id"].str.rstrip(",")
        df["name"] = df["name"].str.rstrip(",")
        df["email"] = df["email"].str.rstrip(",")
        # Typecast
        df["user_id"] = df["user_id"].astype(int)
        df["signup_date"] = pd.to_datetime(df["signup_date"]).dt.date

        self.users_seed = self._as_list_of_tuples(df)

    def load_user_experiments(self):
        """Imports user experiments data from a csv."""

        df = pd.read_csv(
            f"{CURRENT_DIR}/{USER_EXPERIMENTS_FILE}",
            names=[
                "experiment_id",
                "user_id",
                "experiment_compound_ids",
                "experiment_run_time",
            ],
            skiprows=1,
            sep="\t",
        )

        # Clean
        df["experiment_compound_ids"] = df[
            "experiment_compound_ids"
        ].str.rstrip(",")
        df["experiment_id"] = df["experiment_id"].str.rstrip(",")
        df["user_id"] = df["user_id"].str.rstrip(",")
        # Typecast
        df["experiment_id"] = df["experiment_id"].astype(int)
        df["user_id"] = df["user_id"].astype(int)
        df["experiment_run_time"] = df["experiment_run_time"].astype(int)

        self.user_experiments_seed = df

    def load_compounds(self):
        """Imports compounds from a csv."""
        df = pd.read_csv(
            f"{CURRENT_DIR}/{COMPOUNDS_FILE}",
            names=[
                "compound_id",
                "compound_name",
                "copmound_structure",
            ],
            skiprows=1,
            sep="\t",
        )
        # Clean
        df["compound_id"] = df["compound_id"].str.rstrip(",")
        df["compound_name"] = df["compound_name"].str.rstrip(",")

        # Typecast
        df["compound_id"] = df["compound_id"].astype(int)

        self.compounds_seed = self._as_list_of_tuples(df)


# Get all data
seed_data = SeedData()

USER_DATA = seed_data.users_seed
USER_EXPERIMENT_DATA = seed_data.experiment
COMPOUND_DATA = seed_data.compounds_seed
EXPERIMENT_COMPOUND_DATA = seed_data.experiment_compounds

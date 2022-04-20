"""
# Developer: Richard Raphael Banak
# Objective: Class to help manage process automation
# Creation date: 2021-11-15
"""
from google.cloud import bigquery
from google.cloud.exceptions import NotFound
from datetime import datetime
from ds_kit.gcp import big_query as bq


class Process:
    def __init__(self, id_team, id_project, id_process, ds_process):
        self.id_team = id_team
        self.id_project = id_project
        self.id_process = id_process
        self.ds_process = ds_process

        if (
            self.id_team == None
            or self.id_project == None
            or self.id_process == None
            or self.ds_process == None
        ):
            raise Exception("Process parameters not initialized")

        # Data Quality variables
        self.dq_dataset_id = f"{self.id_project}.data_quality"
        self.dq_table_name = f"{self.dq_dataset_id}.data_quality_process"

        if not bq.check_table_exists(self.dq_table_name):
            self.create_data_quality_process_table()

        self.nr_build = self.get_last_build_number() + 1
        self.ds_execution_status = None
        self.ds_observation = None
        self.ds_error_type = None
        self.ds_error_log = None
        self.ds_last_executed_task = None
        self.dt_hr_start_time = datetime.now()
        self.dt_hr_end_time = None
        self.seg_execution_time = None
        self.ds_log_file_path = None

        self.start_process()

    def create_data_quality_process_table(self):

        # if dataset doesn`t exists, create it
        if not bq.check_dataset_exists(dataset_id=self.dq_dataset_id):
            bq.create_dataset(dataset_id=self.dq_dataset_id)

        # if table doesn`t exists, create it
        if not bq.check_table_exists(table_name=self.dq_table_name):
            bq.run_query(
                query=f"""  
                    CREATE TABLE `{self.dq_table_name}`
                    (
                    id_team STRING NOT NULL,
                    id_project STRING NOT NULL,
                    id_process STRING NOT NULL,
                    ds_process STRING NOT NULL,
                    nr_build NUMERIC NOT NULL,
                    ds_execution_status STRING NOT NULL,
                    ds_observation STRING,
                    ds_error_type STRING,
                    ds_error_log STRING,
                    ds_last_executed_task STRING,
                    dt_hr_start_time DATETIME NOT NULL,
                    dt_hr_end_time DATETIME NOT NULL,
                    seg_execution_time NUMERIC NOT NULL,
                    ds_log_file_path STRING,
                    dt_log DATETIME NOT NULL
                    ) """
            )

    def start_process(self):
        print(f"Process: {self.id_process} - {self.ds_process}")
        print(f"Build: {self.nr_build}")
        print(f"Start: {str(self.dt_hr_start_time)}\n")

        if self.ds_last_executed_task:
            print(f"Last task successfully performed: {self.ds_last_executed_task}")

        if self.ds_log_file_path:
            print(f"Log file path: {self.ds_log_file_path}")

        pass

    def finish_process(self):

        # datetime of the end of the process
        self.dt_hr_end_time = datetime.now()

        # time of execution in seconds
        self.seg_execution_time = (
            self.dt_hr_end_time - self.dt_hr_start_time
        ).total_seconds()

        rows_to_insert = [
            {
                "id_team": self.id_team,
                "id_project": self.id_project,
                "id_process": self.id_process,
                "ds_process": self.ds_process,
                "nr_build": self.nr_build,
                "ds_execution_status": self.ds_execution_status,
                "ds_observation": self.ds_observation,
                "ds_error_type": self.ds_error_type,
                "ds_error_log": self.ds_error_log,
                "ds_last_executed_task": self.ds_last_executed_task,
                "dt_hr_start_time": str(self.dt_hr_start_time),
                "dt_hr_end_time": str(self.dt_hr_end_time),
                "seg_execution_time": self.seg_execution_time,
                "ds_log_file_path": self.ds_log_file_path,
                "dt_log": str(datetime.now()),
            },
        ]

        bq.insert_rows_into_table(
            table_id=self.dq_table_name,
            rows_to_insert=rows_to_insert,
        )

        self.show_execution_time()

    def get_last_build_number(self):
        client = bigquery.Client()

        sql = f"""
            SELECT DISTINCT MAX(nr_build) as nr_last_build FROM `{self.dq_table_name}` 
            WHERE id_process = '{self.id_process}' and ds_process = '{self.ds_process}'
        """

        df = client.query(sql).to_dataframe()

        # if build exists, return build, else, return 0
        if df.nr_last_build[0]:
            nr_last_build = int(df.nr_last_build[0])
        else:
            nr_last_build = 0

        return nr_last_build

    def show_execution_time(self):

        duration = self.dt_hr_end_time - self.dt_hr_start_time

        hours = int(duration.seconds / 60 / 60)
        minutes = int((duration.seconds / 60) - (hours * 60))
        seconds = int((duration.seconds) - (minutes * 60) - (hours * 60 * 60))

        timeReport = "Duration: "
        if duration.days:
            timeReport = "{}{} days, ".format(timeReport, duration.days)
        if hours:
            timeReport = "{}{} hour(s), ".format(timeReport, hours)
        if minutes:
            timeReport = "{}{} minute(s), ".format(timeReport, minutes)
        if seconds:
            timeReport = "{}{} second(s).".format(timeReport, seconds)

        print(
            "\nStart of processing: {}".format(
                self.dt_hr_start_time.strftime("%Y-%m-%d %H:%M:%S")
            )
        )
        print(
            "End of the processing: {}".format(
                self.dt_hr_end_time.strftime("%Y-%m-%d %H:%M:%S")
            )
        )

        if duration.seconds == 0:
            print("\nDuration: instant.")
            return
        else:
            print("\n", timeReport, "\n\n")

        print("\n", timeReport, "\n\n")

from quixstreams.sinks.base import BatchingSink, SinkBatch, SinkBackpressureError
import hopsworks
from typing import List
import pandas as pd


class HopsworksFeatureStoreSink(BatchingSink):
    """
    Some sink writing data to a dataframe
    """

    def __init__(
        self,
        api_key: str,
        project_name: str,
        feature_group: str,
        feature_group_verserion: int,
        feature_group_primary_key: List[str],
        feature_group_event_time: str,
    ):
        """
        Establish a connection to Hopsworks Feature Store
        """
        self.api_key = api_key
        self.project_name = project_name
        self.feature_group = feature_group
        self.feature_group_verserion = feature_group_verserion

        # Establish a connection to the HopeWorks Feature Store
        project = hopsworks.login(project=project_name, api_key_value=api_key)
        self._fs = project.get_feature_store()

        # Get the feature group
        self._feature_group = self._fs.get_or_create_feature_group(
            name=feature_group,
            version=feature_group_verserion,
            primary_key=feature_group_primary_key,
            event_time=feature_group_event_time,
            online_enabled=True,
        )

        # call constructor of the base/(parent) class to make sure the batches are initialized
        super().__init__()

    def write(self, batch: SinkBatch):
        # Transform the batch into a pandas DataFrame
        data = [item.value for item in batch]
        data = pd.DataFrame(data)

        # breakpoint()

        try:
            # Try to write data to the db
            self._feature_group.insert(data)
        except Exception as err:  # Capture the original exception
            # In case of timeout, tell the app to wait for 30s
            # and retry the writing later
            raise SinkBackpressureError(
                retry_after=30.0,
                topic=batch.topic,
                partition=batch.partition,
            ) from err  # Chain the exception

from typing import (List, Dict)

import ray
from ray._raylet import (
    PlacementGroupID, )


def placement_group(bundles: List[Dict[str, float]],
                    strategy: str = "PACK",
                    name: str = "unnamed_group"):
    """
    Create a placement group.

    This method is the api to create placement group.

    Args:
        bundles: A list of bundles which represent the resources needed.
        strategy: The strategy to create the placement group.
            PACK: Packs Bundles into as few nodes as possible.
            SPREAD: Places Bundles across distinct nodes as even as possible.
            STRICT_PACK: Packs Bundles into one node.
            STRICT_SPREAD: Packs Bundles across distinct nodes.
            The group is not allowed to span multiple nodes.
        name: The name of the placement group.
    """
    worker = ray.worker.global_worker
    worker.check_connected()

    if not isinstance(bundles, list):
        raise ValueError(
            "The type of bundles must be list, got {}".format(bundles))

    placement_group_id = worker.core_worker.create_placement_group(
        name, bundles, strategy)

    return placement_group_id


def remove_placement_group(placement_group_id: PlacementGroupID):
    assert type(placement_group_id) == PlacementGroupID
    worker = ray.worker.global_worker
    worker.check_connected()

    worker.core_worker.remove_placement_group(placement_group_id)


def placement_group_table(placement_group_id):
    assert placement_group_id is not None
    worker = ray.worker.global_worker
    worker.check_connected()
    return ray.state.state.placement_group_table(placement_group_id)


### TESTS ###

# A method which asserts equality between an ordered dict of numpy arrays and another
# ordered dict - WTH
import collections

from herobraine.hero.spaces import Dict
from herobraine.hero.test_spaces import assert_equal_recursive
from herobraine.wrappers.vector_wrapper import VecWrapper
from herobraine.wrappers.vector_obfuscation_wrapper import VectorObfWrapper
import herobraine.env_specs as envs
from herobraine.wrappers.util import union_spaces
import numpy as np


def test_obf_wrapper(base_env=envs.MINERL_OBTAIN_DIAMOND_V0, common_env=None):
    """
    Tests that wrap_action composed with unwrap action is the identity.
    1. Construct an VecWrapper of an EnvSpec called ObtainDiamond
    2. Sample actions from its action space
    3. Wrap and unwrap those actions.
    4. Assert that the result is the same as the sample
    """
    vec_env = VectorObfWrapper(VecWrapper(base_env, common_env))

    s = base_env.get_action_space().sample()
    ws = vec_env.wrap_action(s)
    us = vec_env.unwrap_action(ws)
    assert_equal_recursive(s, us)


def test_wrap_unwrap_action(base_env=envs.MINERL_OBTAIN_DIAMOND_V0, common_env=None):
    """
    Tests that wrap_action composed with unwrap action is the identity.
    1. Construct an VecWrapper of an EnvSpec called ObtainDiamond
    2. Sample actions from its action space
    3. Wrap and unwrap those actions.
    4. Assert that the result is the same as the sample
    """
    vec_env = VecWrapper(base_env, common_env)

    s = base_env.get_action_space().sample()
    ws = vec_env.wrap_action(s)
    us = vec_env.unwrap_action(ws)
    assert_equal_recursive(s, us)

    if common_env is not None:
        s = base_env.get_action_space().sample()
        ws = vec_env.wrap_action(s)
        us = vec_env.unwrap_action(ws)
        assert_equal_recursive(s, us)


def test_wrap_unwrap_action_treechop():
    test_wrap_unwrap_action(base_env=envs.MINERL_TREECHOP_V0)


def test_wrap_unwrap_action_navigate():
    test_wrap_unwrap_action(base_env=envs.MINERL_NAVIGATE_DENSE_EXTREME_V0)


def test_wrap_unwrap_observation(base_env=envs.MINERL_OBTAIN_DIAMOND_V0, common_env=None):
    """
    Tests that wrap_observation composed with unwrap observation is the identity.
    1. Construct an VecWrapper of an EnvSpec called ObtainDiamond
    2. Sample observation from its observation space
    3. Wrap and unwrap those observations.
    4. Assert that the result is the same as the sample
    """
    vec_env = VecWrapper(base_env, common_env)

    s = base_env.get_observation_space().sample()
    ws = vec_env.wrap_observation(s)
    us = vec_env.unwrap_observation(ws)
    assert_equal_recursive(s, us)

    if common_env is not None:
        s = common_env.get_observation_space().sample()
        ws = vec_env.wrap_observation(s)
        us = vec_env.unwrap_observation(ws)
        assert_equal_recursive(s, us)


def test_wrap_unwrap_observation_treechop():
    test_wrap_unwrap_observation(base_env=envs.MINERL_TREECHOP_V0)


def test_wrap_unwrap_observation_navigate():
    test_wrap_unwrap_observation(base_env=envs.MINERL_NAVIGATE_DENSE_EXTREME_V0)


def test_vector_action_space(base_env=envs.MINERL_OBTAIN_DIAMOND_V0, common_env=None):
    vec_env = VecWrapper(base_env, common_env)
    assert isinstance(vec_env.get_action_space(), Dict)
    assert isinstance(vec_env.get_observation_space(), Dict)
    print(vec_env.get_action_space())
    print(vec_env.get_action_space().spaces)
    assert ('vector' in vec_env.get_action_space().spaces)
    assert ('vector' in vec_env.get_observation_space().spaces)


def test_diamond_space():
    test_vector_action_space(envs.MINERL_OBTAIN_DIAMOND_V0)


def test_union_spaces():
    act_1 = envs.MINERL_TREECHOP_V0.actionables
    act_2 = envs.MINERL_NAVIGATE_DENSE_V0.actionables
    for space in union_spaces(act_2, act_1):
        assert(space in act_1 or space in act_2)
    for space in act_1:
        assert(space in union_spaces(act_1, act_2))
    for space in act_2:
        assert(space in union_spaces(act_2, act_1))


def test_vec_wrapping_with_common_envs():
    base_env = envs.MINERL_TREECHOP_V0
    common_env = envs.MINERL_NAVIGATE_DENSE_V0

    test_wrap_unwrap_observation(base_env, common_env)
    test_wrap_unwrap_action(base_env, common_env)

    base_env = envs.MINERL_OBTAIN_DIAMOND_V0
    common_env = envs.MINERL_NAVIGATE_DENSE_V0

    test_wrap_unwrap_observation(base_env, common_env)
    test_wrap_unwrap_action(base_env, common_env)

    base_env = envs.MINERL_OBTAIN_IRON_PICKAXE_V0
    common_env = envs.MINERL_OBTAIN_DIAMOND_V0

    test_wrap_unwrap_observation(base_env, common_env)
    test_wrap_unwrap_action(base_env, common_env)
from hypothesis import given
from hypothesis import strategies as st

from game.core.models import EntityAttr, SpriteState


@given(st.builds(EntityAttr))
def test_entity_attr(entity_attr):
    assert entity_attr.dict()  # Verify serialization


@given(st.builds(SpriteState))
def test_sprite_state(sprite_state):
    assert sprite_state.dict()  # Verify serialization

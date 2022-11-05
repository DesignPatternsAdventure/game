from hypothesis import given
from hypothesis import strategies as st

from game.core.models import SpriteState


@given(st.builds(SpriteState))
def test_sprite_state(sprite_state):
    assert sprite_state.dict()  # Verify serialization

from aiogram.dispatcher.filters.state import State, StatesGroup


class adding_sample(StatesGroup):
    sample_id = State()
    sample = State()

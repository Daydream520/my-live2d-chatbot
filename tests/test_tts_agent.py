import pytest
from unittest.mock import MagicMock
from src.agents.tts_agent import TTSAgent
import pygame # Import it to reference its exceptions

# It's better to patch where the object is used.
# All dependencies are used inside 'src.agents.tts_agent'.
TTS_AGENT_PATH = 'src.agents.tts_agent'

@pytest.fixture(autouse=True)
def mock_pygame(mocker):
    """Automatically mock all pygame functions for every test."""
    mocker.patch(f'{TTS_AGENT_PATH}.pygame.mixer.init', return_value=None)
    mocker.patch(f'{TTS_AGENT_PATH}.pygame.mixer.music.load')
    mocker.patch(f'{TTS_AGENT_PATH}.pygame.mixer.music.play')
    # Let's make the side effect simpler for now. It needs to be iterable.
    mocker.patch(f'{TTS_AGENT_PATH}.pygame.mixer.music.get_busy', side_effect=[True, True, False])
    mocker.patch(f'{TTS_AGENT_PATH}.pygame.mixer.music.unload')

@pytest.fixture
def mock_dependencies(mocker):
    """Mock other dependencies like gTTS, threading, file I/O, etc."""
    mock_gtts = mocker.patch(f'{TTS_AGENT_PATH}.gTTS')
    mock_gtts_instance = MagicMock()
    mock_gtts.return_value = mock_gtts_instance

    mock_temp_file = MagicMock()
    mock_temp_file.name = "/tmp/mock_audio.mp3"
    # The agent code closes the file handle right away. Let's mock that.
    mock_temp_file.close = MagicMock()
    mocker.patch(f'{TTS_AGENT_PATH}.tempfile.NamedTemporaryFile', return_value=mock_temp_file)

    mock_os_unlink = mocker.patch(f'{TTS_AGENT_PATH}.os.unlink')

    mock_thread_class = mocker.patch(f'{TTS_AGENT_PATH}.threading.Thread')

    mock_time_sleep = mocker.patch(f'{TTS_AGENT_PATH}.time.sleep')

    return {
        "gtts": mock_gtts,
        "gtts_instance": mock_gtts_instance,
        "os_unlink": mock_os_unlink,
        "thread": mock_thread_class,
        "temp_filename": mock_temp_file.name,
        "sleep": mock_time_sleep,
    }


def test_speak_logic(mocker, mock_dependencies):
    """
    Tests the TTSAgent.speak() method's logic, ensuring all dependencies
    are called correctly and cleanup is performed.
    """
    # Arrange
    agent = TTSAgent()
    test_text = "hello world"

    # Act
    agent.speak(test_text)

    # Assertions for the main speak method
    mock_dependencies["gtts"].assert_called_once_with(text=test_text, lang='zh-tw')
    mock_dependencies["gtts_instance"].save.assert_called_once_with(mock_dependencies["temp_filename"])

    # Use the patched objects directly for assertion
    pygame.mixer.music.load.assert_called_once_with(mock_dependencies["temp_filename"])
    pygame.mixer.music.play.assert_called_once()

    # Check that the cleanup thread was started
    mock_dependencies["thread"].assert_called_once()
    thread_args = mock_dependencies["thread"].call_args

    # Extract target and args for the cleanup task
    cleanup_task_func = thread_args.kwargs['target']
    cleanup_task_args = thread_args.kwargs['args']
    assert cleanup_task_func == agent._cleanup_task
    assert cleanup_task_args == (mock_dependencies["temp_filename"],)

    # --- Test the cleanup task itself ---

    # Act: Run the cleanup task synchronously
    cleanup_task_func(*cleanup_task_args)

    # Assertions for the cleanup task
    assert mock_dependencies["sleep"].call_count == 3  # Called in the while loop and once after

    # Check that the music was unloaded
    pygame.mixer.music.unload.assert_called_once()

    # Check that the file was unlinked (deleted)
    mock_dependencies["os_unlink"].assert_called_once_with(mock_dependencies["temp_filename"])

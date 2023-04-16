from enum import Enum

from loguru import logger
import edge_tts


class EdgeTtsVoice(Enum):
    xiaoxiao = "zh-CN-XiaoxiaoNeural"
    xiaoyi = "zh-CN-XiaoyiNeural"
    yunjian = "zh-CN-YunjianNeural"
    yunxi = "zh-CN-YunxiNeural"
    yunxia = "zh-CN-YunxiaNeural"
    yunyang = "zh-CN-YunyangNeural"
    liaoning = "zh-CN-liaoning-XiaobeiNeural"
    shanxi = "zh-CN-shaanxi-XiaoniNeural"


def from_voice(value: str):
    for voice in EdgeTtsVoice.__members__.values():
        if voice.value.lower() == value.lower():
            return voice
    return None


def supported_tts_info():
    names = []
    for voice in EdgeTtsVoice.__members__.values():
        names.append(voice.name)
    return ', '.join(names)


async def edge_tts_speech(text: str, voice_name: str, path: str):
    try:
        communicate = edge_tts.Communicate(text, voice_name)
        await communicate.save(f"{path}.mp3")
        return True
    except ValueError as e:
        if str(e).startswith("Invalid voice"):
            raise ValueError(
                f"不支持的音色：{voice_name}"
                + "\n音色列表："
                + str(await edge_tts.list_voices())
            )
    except Exception as err:
        logger.exception(err)
        logger.error("[Edge TTS] API error: ", err)
        return False

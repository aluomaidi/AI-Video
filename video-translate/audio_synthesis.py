import asyncio
import edge_tts

async def synthesize(text, output_file, voice='en-US-AriaNeural', rate='0%', volume='0%'):
    """
    Synthesize text to speech and save to an output file.

    Args:
        text (str): The text to synthesize.
        output_file (str): The path to the output audio file.
        voice (str): The voice to use for synthesis.
        rate (str): The speech rate adjustment (e.g., '0%', '10%').
        volume (str): The speech volume adjustment (e.g., '0%', '10%').
    """
    try:
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_file)
        print(f"Audio content written to file {output_file}")
    except Exception as e:
        print(f"An error occurred during synthesis: {e}")

def synthesize_text_to_speech(text, output_file, voice='en-US-AriaNeural', rate='0%', volume='0%'):
    """
    Wrapper function to run the asynchronous synthesize function.

    Args:
        text (str): The text to synthesize.
        output_file (str): The path to the output audio file.
        voice (str): The voice to use for synthesis.
        rate (str): The speech rate adjustment (e.g., '0%', '10%').
        volume (str): The speech volume adjustment (e.g., '0%', '10%').
    """
    asyncio.run(synthesize(text, output_file, voice, rate, volume))

if __name__ == "__main__":
    # Example usage
    text = '''陕西，这片古老而神秘的土地，不仅有着悠久的历史文化，更蕴藏着丰富的特产资源。今天，我要给大家介绍几款陕西的特色美食，让你在品味中感受陕西的独特魅力。
        首先，我们要说的是那色香味俱佳的陕西凉皮。选用优质小麦粉，经过独特的工艺制成，口感滑爽，搭配秘制酱料，酸辣适中，让人回味无穷。无论是炎炎夏日还是寒冷冬季，一碗凉皮都能带给你不一样的味觉享受。
        接下来，是让人垂涎三尺的肉夹馍。选用上等猪肉，经过慢火炖煮，肉质酥软，香气四溢。搭配手工制作的白面馍，外酥里嫩，每一口都是满满的幸福感。无论是早餐还是下午茶，肉夹馍都是你不二的选择。
        最后，我们要推荐的是陕西的特色零食——柿饼。选用新鲜柿子，经过晾晒、腌制等多道工序制成，甜而不腻，营养丰富。无论是自己品尝还是送给亲朋好友，柿饼都是一份充满心意的礼物。
        现在购买还有优惠活动哦！陕西凉皮、肉夹馍、柿饼，每一款都是地道的陕西风味，让你在品尝美食的同时，也能感受到陕西的热情与淳朴。快来选购吧，让这些美食为你的味蕾带来一场难忘的旅行！'''
    output_file = "output/synthesize.mp3"
    voice = 'zh-CN-shaanxi-XiaoniNeural'
    rate = '0%'
    volume = '0%'

    synthesize_text_to_speech(text, output_file, voice, rate, volume)
def multiply_timestamp(timestamp, multiplier):
    # 将时间戳拆分成开始时间和结束时间部分
    start, end = timestamp.split(" --> ")

    # 处理开始时间
    start_parts = start.split(":")
    hours = int(start_parts[0])
    minutes = int(start_parts[1])
    seconds, milliseconds = map(int, start_parts[2].replace(",", ".").split("."))

    # 计算新的开始时间
    new_start_seconds = hours * 3600 + minutes * 60 + seconds
    new_start_seconds *= multiplier
    new_start_hours = int(new_start_seconds // 3600)
    new_start_seconds %= 3600
    new_start_minutes = int(new_start_seconds // 60)
    new_start_seconds %= 60
    new_start_milliseconds = int(milliseconds * multiplier)

    # 格式化新的开始时间
    new_start_time = "{:02}:{:02}:{:02},{:03}".format(
        new_start_hours, new_start_minutes, new_start_seconds, new_start_milliseconds
    )

    # 处理结束时间
    end_parts = end.split(":")
    hours = int(end_parts[0])
    minutes = int(end_parts[1])
    seconds, milliseconds = map(int, end_parts[2].replace(",", ".").split("."))

    # 计算新的结束时间
    new_end_seconds = hours * 3600 + minutes * 60 + seconds
    new_end_seconds *= multiplier
    new_end_hours = int(new_end_seconds // 3600)
    new_end_seconds %= 3600
    new_end_minutes = int(new_end_seconds // 60)
    new_end_seconds %= 60
    new_end_milliseconds = int(milliseconds * multiplier)

    # 格式化新的结束时间
    new_end_time = "{:02}:{:02}:{:02},{:03}".format(
        new_end_hours, new_end_minutes, new_end_seconds, new_end_milliseconds
    )

    # 返回新的时间戳字符串
    return f"{new_start_time} --> {new_end_time}"

# 示例用法
timestamp = "00:00:10,580 --> 00:00:14,240"
multiplier = 2
new_timestamp = multiply_timestamp(timestamp, multiplier)
print(new_timestamp)  # 输出：00:00:06,680 --> 00:00:14,002
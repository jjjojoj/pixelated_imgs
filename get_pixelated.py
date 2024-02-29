from PIL import Image, ImageDraw, ImageStat
import os


# pixelated+black_background
def c_b_b(i, f, r, o):
    output_image = Image.new("RGB", i.size)
    draw = ImageDraw.Draw(output_image)
    for x in range(0, i.width, r * 2 + o):
        for y in range(0, i.height,
                       r * 2 + o):
            box = (x, y, x + r * 2, y + r * 2)
            region = i.crop(box)
            stat = ImageStat.Stat(region)
            average_color = tuple(int(c) for c in stat.median)
            draw.ellipse(box, fill=average_color)
    output_image.save(f'pixelated_b{f}')


# cut into small circles with black_background
def s_i_c(i, f, r, o):
    output_image = Image.new("RGB", i.size,
                             (0, 0, 0, 255))
    width, height = i.size
    for x in range(0, width, r * 2 + o):
        for y in range(0, height, r * 2 + o):
            box = (x, y, x + r * 2, y + r * 2)
            mask = Image.new('L', (
                r * 2, r * 2), 0)
            draw_mask = ImageDraw.Draw(mask)
            draw_mask.ellipse((0, 0, r * 2, r * 2), fill=255)
            region = i.crop(box)
            region.putalpha(mask)
            output_image.paste(region, box, region)
    output_image.save(f'circles{f}')


# pixelated + average_color_background
def p_c_i_b(i, f, r, o):
    output_image = Image.new("RGB", i.size,
                             i.getpixel((0, 0)))
    draw = ImageDraw.Draw(output_image)
    for x in range(0, i.width, r * 2 + o):
        for y in range(0, i.height, r * 2 + o):
            box = (x, y, x + r * 2, y + r * 2)
            region = i.crop(box)
            average_color = tuple(
                int(sum(channel) / len(channel))
                for channel in
                zip(*region.getdata()))
            draw.ellipse(box, fill=average_color)
    output_image.save(f'pixelated_a{f}')


# pixelated + original_background
def p_w_c(i, f, r, o):
    width, height = i.size
    output_image = Image.new("RGB", i.size)
    draw = ImageDraw.Draw(output_image)

    for x in range(0, width, r):
        for y in range(0, height, r):
            box = (x, y, x + r, y + r)
            region = i.crop(box)
            average_color = tuple(
                int(sum(channel) / len(channel)) for channel in
                zip(*region.getdata()))
            draw.rectangle(box, fill=average_color)
            center = (
                (box[0] + box[2]) // 2, (box[1] + box[3]) // 2)
            ra = (r - o) // 2  # circle spacing

            draw.ellipse(
                (center[0] - ra, center[1] - ra,
                 center[0] + ra, center[1] +
                 ra), outline=(0, 0, 0),
                width=1)  # width of the circles outline
    output_image.save(f'pixelated_o{f}')


radius = 30  # radius
offset = 4  # spacing

folder_path = 'imgs'
for filename in os.listdir(folder_path):
    if filename.lower().endswith(
            ('.png', '.jpg', '.jpeg', '.gif')):
        file_path = os.path.join(folder_path, filename)
        image = Image.open(file_path)
        c_b_b(image, filename, radius, offset)
        s_i_c(image, filename, radius, offset)
        p_c_i_b(image, filename, radius, offset)
        p_w_c(image, filename, radius * 2, offset * 2)

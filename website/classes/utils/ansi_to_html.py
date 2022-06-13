import re

def ansi_to_html(ansi):
    try:
        pattern = r'\x1B\[38;2;([0-9]{1,3});([0-9]{1,3});([0-9]{1,3})m'
        regex = re.compile(pattern)
        result = regex.findall(ansi)
        out = ansi
        for res in result:
            R = int(res[0])
            G = int(res[1])
            B = int(res[2])
            R = max(0, min(255, R))
            G = max(0, min(255, G))
            B = max(0, min(255, B))
            color = "#"+("000" + hex(((R*256)+G)*256+B)[2:])[-6:].upper()
            # Replace regex group
            str_to_replace = f"\x1B[38;2;{R};{G};{B}m"
            html_str       = f"</span><span style=\"color:{color}\">"
            out = out.replace(str_to_replace, html_str, 1)
        out = out.replace("\x1B[0m", f"</span>", 1)
        out = "<span>" + out
        return out

    except Exception as e:
        print(e)

#ansi="|START|\33[38;2;32;206;128mclr1|\33[38;2;128;32;206mclr2|\33[38;2;206;128;32mclr3|\33[0mEND|"
#html = ansi_to_html(ansi)
#print(html)

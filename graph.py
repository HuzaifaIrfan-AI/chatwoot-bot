from bot import bot

if __name__ == "__main__":
    png_bytes = bot.get_graph().draw_mermaid_png()
    # Write the bytes to a file
    with open("langgraph_output.png", "wb") as f:
        f.write(png_bytes)
from intent.aura_intent import AuraIntentRouter
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich import box

router = AuraIntentRouter()
console = Console()

def pretty_output(user, result):
    user_text = Text(f"USER: {user}", style="bold cyan")
    result_text = Text(f"{result}", style="bold green")

    panel = Panel.fit(
        Text.assemble(
            ("USER:\n", "bold cyan"),
            (f"  {user}\n\n", "white"),
            ("ROUTER OUTPUT:\n", "bold yellow"),
            (f"  {result}", "green"),
        ),
        title="✨ AURA Intent Router",
        subtitle="Debug Output",
        border_style="magenta",
        padding=(1, 2),
        box=box.ROUNDED
    )

    console.print(panel)
    console.print("\n")  # spacing

def test_query(q):
    out = router.route(q)
    pretty_output(q, out)


def main():
    for query in (
        "Aura show me what you see.",
        "Is it hot in here?",
        "Who made you?",
        "Take a picture.",
        "What is in front of me right now?",
        "What's the room temperature?",
        "Check the sensor reading.",
        "Tell me a joke.",
    ):
        test_query(query)


if __name__ == "__main__":
    main()

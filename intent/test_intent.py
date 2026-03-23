from aura_intent import AuraIntentRouter
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


# -------------------------
# Run test cases
# -------------------------
test_query("Aura show me what you see.")
test_query("Is it hot in here?")
test_query("Who made you?")


test_query("Take a picture.")
test_query("What is in front of me right now?")

test_query("What's the room temperature?")

test_query("Check the sensor reading.")

test_query("Tell me a joke.")
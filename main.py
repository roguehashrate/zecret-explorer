import requests
import datetime
from rich.console import Console
from rich.table import Table
from rich.text import Text

API_BASE = "https://blockbook.zec.zelcore.io/api/v2"
console = Console()

def fetch_block_details(block_identifier):
    url = f"{API_BASE}/block/{block_identifier}"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()

def zatoshi_to_zec(value_str):
    try:
        value = int(value_str)
        return f"{value / 1e8:.8f} ZEC"
    except Exception:
        return value_str

def format_timestamp(ts):
    try:
        dt = datetime.datetime.fromtimestamp(int(ts))
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return str(ts)

def display_block_info(block):
    # Block summary table
    table = Table(title="Block Summary", style="bold cyan")
    table.add_column("Field", style="bold magenta")
    table.add_column("Value", style="bold white")

    def add_row(field, value):
        if isinstance(value, int):
            value = f"{value:,}"
        table.add_row(field, str(value))

    add_row("Hash", block.get("hash"))
    add_row("Previous Block Hash", block.get("previousBlockHash"))
    add_row("Next Block Hash", block.get("nextBlockHash"))
    add_row("Height", block.get("height"))
    add_row("Confirmations", block.get("confirmations"))
    add_row("Size (bytes)", block.get("size"))
    add_row("Merkle Root", block.get("merkleRoot"))
    add_row("Nonce", block.get("nonce"))
    difficulty = block.get("difficulty")
    if difficulty:
        difficulty_str = f"{float(difficulty):,.2f}"
        add_row("Difficulty", difficulty_str)
    add_row("Transaction Count", block.get("txCount"))
    block_time = block.get("time") or block.get("blockTime", 0)
    add_row("Block Time", format_timestamp(block_time))

    console.print(table)

    # Transactions
    txs = block.get("txs", [])
    if not txs:
        console.print("\n[red]No transactions in this block.[/red]")
        return

    for i, tx in enumerate(txs, 1):
        tx_table = Table(title=f"Transaction {i}", style="bold green")
        tx_table.add_column("Field", style="bold yellow")
        tx_table.add_column("Value", style="white")

        def add_tx_row(field, value):
            if isinstance(value, int):
                value = f"{value:,}"
            elif field in ["Value In", "Value Out", "Fees"]:
                value = zatoshi_to_zec(str(value))
            elif field == "Block Time":
                value = format_timestamp(value)
            tx_table.add_row(field, str(value))

        add_tx_row("TxID", tx.get("txid"))
        add_tx_row("Block Hash", tx.get("blockHash"))
        add_tx_row("Block Height", tx.get("blockHeight"))
        add_tx_row("Confirmations", tx.get("confirmations"))
        add_tx_row("Block Time", tx.get("blockTime"))
        add_tx_row("Value In", tx.get("valueIn", "0"))
        add_tx_row("Value Out", tx.get("value", "0"))
        add_tx_row("Fees", tx.get("fees", "0"))

        console.print(tx_table)

        # Outputs table
        vouts = tx.get("vout", [])
        if vouts:
            outputs_table = Table(title="Outputs", show_lines=True, style="bold blue")
            outputs_table.add_column("Index", style="bold cyan", justify="right")
            outputs_table.add_column("Value", style="bold white")
            outputs_table.add_column("Address", style="bold magenta")

            for v in vouts:
                addr = ", ".join(v.get("addresses", [])) if v.get("isAddress") else "N/A"
                value = zatoshi_to_zec(v.get("value", "0"))
                outputs_table.add_row(str(v.get("n")), value, addr)

            console.print(outputs_table)

def main():
    block_input = input("Enter block hash or height: ").strip()
    try:
        block_info = fetch_block_details(block_input)
    except Exception as e:
        console.print(f"[red]Error fetching block details: {e}[/red]")
        return

    for key in ["page", "totalPages", "itemsOnPage", "version", "bits"]:
        block_info.pop(key, None)

    display_block_info(block_info)

if __name__ == "__main__":
    main()

import os
import json
from web3 import Web3
from web3.exceptions import Web3ValidationError
from tkinter import Tk, messagebox

def execWeb3(address):
    web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
    checksum_address = Web3.to_checksum_address(address)
    abi_path = os.path.join(os.path.dirname(__file__), "/home/admin/blockchainApp/frontend/abi/sendETH3.sol/sendETH3.json")
    with open(abi_path, "r") as abi_file:
        data = json.load(abi_file)
        contract_abi = data['abi']
    contract_instance = web3.eth.contract(address=checksum_address, abi=contract_abi)
    return contract_instance, web3

# Tkinterダイアログボックスを表示し、ユーザーからの指示を待つ
def get_user_confirmation():
    root = Tk()
    root.withdraw()  # ルートウィンドウを非表示に
    response = messagebox.askyesno("confirmation", "Should I execute a smart contract?")
    root.destroy()
    return response

def main(address: str, amount: int, recipient: str):
    if get_user_confirmation():
        try:
            contract_instance, web3 = execWeb3(address)

            # recipientのアドレスをchecksum address形式に変換
            recipient_checksum = Web3.to_checksum_address(recipient)
            checksum_address = Web3.to_checksum_address(address)
            
            
            # 送金前の残高を取得（送金元、送金先）
            balance_sender_before = contract_instance.functions.balanceOf(checksum_address)
            balance_recipient_before = contract_instance.functions.balanceOf(recipient_checksum)
            

            
            # amountをETHからWeiに変換（もしETH単位で渡されている場合）
            amount_wei = Web3.to_wei(amount, 'ether')
            tx_hash = contract_instance.functions.approveAndSend(recipient_checksum, amount).transact({'from': checksum_address})
            tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
            
            # 送金後のトークン残高を取得（送金元、送金先）
            balance_sender_after = contract_instance.functions.balanceOf(checksum_address)
            balance_recipient_after = contract_instance.functions.balanceOf(recipient_checksum)

            result = {
                "status": "success",
                "message": "処理が成功しました",
                "balanceSenderBefore": balance_sender_before,
                "balanceSenderAfter": balance_sender_after,
                "balanceRecipientBefore": balance_recipient_before,
                "balanceRecipientAfter": balance_recipient_after
            }
            return result
        except Web3ValidationError as e:
            return {"status": "error", "message": str(e)}
    else:
        return {"status": "denied", "message": "ユーザーによって操作が拒否されました。"}
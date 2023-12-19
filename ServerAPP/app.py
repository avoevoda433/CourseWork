import asyncio
from flask import Flask, request, Response, stream_with_context, jsonify
import requests
import json
import socket
from scapy.all import srp
from scapy.layers.l2 import ARP, Ether


def get_host_name(ip):
    try:
        host_name = socket.gethostbyaddr(ip)[0]
        return host_name
    except (socket.herror, socket.gaierror):
        return None


app = Flask(__name__)


def send_api_request(ip):
    url = f"http://{ip}/get_info"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return ip, response.json()
    except requests.RequestException as e:
        return ip, {"error": str(e)}


def scan_host(ip):
    results = []
    try:
        arp_request = ARP(pdst=ip)
        ether = Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = ether / arp_request

        answered, _ = srp(packet, timeout=1, verbose=0)

        for sent, received in answered:
            ip_address = received.psrc
            host_name = get_host_name(ip_address)
            results.append({"ip": ip_address, "hostname": host_name})

    except Exception as e:
        results.append({"ip": ip, "hostname": None, "error": str(e)})

    return results

@app.route('/computers', methods=['GET'])
def scan():
    ip_range = request.args.get('ip_range', '')
    result_data = scan_host(ip_range)
    return jsonify(result_data)



@app.route('/computer', methods=['GET'])
def get_computers():
    ip = request.args.get('ip', '127.0.0.1')
    _, answer = send_api_request(ip)
    return answer


@app.route('/check', methods=['GET'])
def check():
    return Response(status=200)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)

============
Support test
============

Run
===

使い方

.. code-block:: shell

	cd konnolab
	ansible-playbook -i hosts.yaml salvage-log-playbook.yml -e "ansible_sudo_pass=secret"

接続先のマシンでsudoのパスワードが必要ない場合は，``-e "ansible_sudo_pass=secret"``　は不要

Setup
=====

.. code-block:: shell

	cd konnolab
	pip install -r requirements.txt
	pip install ansible

Files
=====

play-book
---------
- hosts.yaml ターゲットの情報

.. code-block:: yaml
	
	devices:
		hosts:
	  	PC: 
	    	ansible_host: 192.168.1.102
			  ansible_port: 22  
			  ansible_user: pi  
			  ansible_password: passwd
			  tftp_host: 192.168.1.101
			  ap_host: 192.168.1.100
			  ap_port: 22
			  ap_user: admin
			  ap_password: admin123
			  iperf_port: 5001
			  
	PCはマシン名
  下はAnsibleがマシンにSSHでログインするときに利用
  ansible_hostはマシンのIPアドレス
	ansible_portはマシンのポート  
	ansible_userはユーザー名 
	ansible_passwordはパスワード

	iperf_portはこのマシンの iperfが使うポート
	tftp_hostはAPが利用するTFTPサーバのアドレス，通常このansible_hostと同じ

	下はマシンからAPにSSHでログインするときに利用
	ap_hostはAPのIPアドレス
	ap_portはAPのポート
	ap_userはAPのユーザー名
	ap_passwordはAPのパスワード
	
- setup-playbook.yml　セットアップとかする

	- tftp-hpa, iperf3, python3-pip, netmikoのインストール
	- tasks：ターゲットマシンで使うスクリプトをターゲットマシンにコピー
	
- run-test-service-playbook.yml tftpdとiperfの起動

	- iperfは30分間バックグラウンドで動く
	
- pktcap-playbook.yml パケットキャプチャをAPで行う
	
	- APにデバッグ設定する．logging on, logging console debugging
	- パケットキャプチャをする．rim wireless radio 2で10000発．バックグラウンドで30分間経つと10000発に到達しなくても止まる．キャプチャはtftp_hostで指定したところに書き込まれる．
	
- salvage-log-playbook.yml ログファイル，テックサポートをAnsibleホストに集める．	


tasks
-----

- configure_ap.py
		APにデバッグ設定する．
		
- get_tech.py
		テックサポートの取得．tftp_hostに持ってくる．
		
- run_pktcap.py
		パケットキャプチャする．
		
exping-csv.py
-------------

expingのCSVファイルで10発づつまとめて何発落ちたかを"*"の数で，10発打った時間の相加平均の時間で表示することによりデリバティブ的な感じでヤバい時間をなんとなく掴む

**使い方** 

``python exping-csv.py <expingの結果.csv>``

.. code-block::

	2020/04/17 19:22:44 ping lost :
	2020/04/17 19:22:46 ping lost :
	2020/04/17 19:22:49 ping lost :
	2020/04/17 19:22:53 ping lost :*********
	2020/04/17 19:22:58 ping lost 10 times continuously
	2020/04/17 19:23:01 ping lost :*
	2020/04/17 19:23:04 ping lost :
	2020/04/17 19:23:07 ping lost :***
	2020/04/17 19:23:11 ping lost 10 times continuously
	2020/04/17 19:23:16 ping lost 10 times continuously
	2020/04/17 19:23:20 ping lost :***
	2020/04/17 19:23:23 ping lost :
	2020/04/17 19:23:25 ping lost :***
	2020/04/17 19:23:30 ping lost :*****
	2020/04/17 19:23:32 ping lost :
	2020/04/17 19:23:35 ping lost :
	2020/04/17 19:23:37 ping lost :



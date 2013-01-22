from peewee import *
from datetime import date
import random

db = SqliteDatabase('brender.sqlite')

class Clients(Model):
    mac_address = IntegerField()
    hostname = CharField()
    status = CharField()
    warning = BooleanField()
    config = CharField()

    class Meta:
        database = db

class Orders(Model):
    client = ForeignKeyField(Clients, related_name='fk_client')
    order = CharField()

    class Meta:
        database = db


def create_databases():
	"""Create the required databases during installation.

	Based on the classes specified above (currently Clients and Orders)
	"""
	Clients.create_table()
	Orders.create_table()


def create_clients(clients_amount):
	"""Create the specified amount of clients.

	Assigns some random values as hostname and mac_address. Used only
	for testing purposes.
	"""
	for i in range(clients_amount):
		Clients.create(mac_address = 123 + i,
			hostname = 'client_' + str(i),
			status = 'enabled',
			warning = False,
			config ='JSON string')
	print("Database filled with " + str(clients_amount) + " clients.")


def remove_clients():
	"""Removes all clients found in the clients table.

	Should be refactored?
	"""
	clients_count = Clients.select().count()
	for client in Clients.select():
		print("Removing client " + client.hostname)
		client.delete_instance()
	print("Removed all the " + str(clients_count) + " clients")


def create_orders(orders_amount):
	"""Creates the specified amount of orders.

	Orders are fake and get randomly assigned do the existing clients
	by picking their row id from a list generate on the fly.
	"""
	clients_count = Clients.select().count()
	if clients_count > 0:
		# We build an index of the client ids
		client_ids = []
		for client in Clients.select():
			client_ids.append(client.id)

		for i in range(orders_amount):
			random_id = random.choice(client_ids)
			Orders.create(client = random_id,
				order = "hello " + str(random_id))

		print("Added " + str(orders_amount) + " orders.")
	else:
		print("[warning] No clients available")


def disable_clients():
	for client in Clients.select():
		client.status = 'disabled'
		client.save()
		print("Changing status to 'disabled' for client " + str(client.hostname))


def load_clients():
	clients_list = []
	for client in Clients.select():
		clients_list.append(client)
	
	return clients_list


def create_client(attributes):
	new_client = Clients.create(mac_address = attributes['mac_address'],
		hostname = attributes['hostname'],
		status = attributes['status'],
		warning = attributes['warning'],
		config =attributes['config'])
	print("New client " + attributes['hostname'] + " was added")
	return new_client


def show_clients():
	for client in Clients.select():
		print client.hostname, client.fk_client.count(), 'fk_client'
		for order in client.fk_client:
			print '    ', order.order


def save_runtime_client(client):
	db_client = Clients.get(Clients.id == client.get_attributes('id'))
	db_client.hostname = client.get_attributes('hostname')
	db_client.status = client.get_attributes('status')
	db_client.warning = client.get_attributes('warning')
	db_client.config = client.get_attributes('config')
	db_client.save()

#create_databases()

#create_clients(10)
#remove_clients()
#create_orders(5)
#disable_clients()

#show_clients()
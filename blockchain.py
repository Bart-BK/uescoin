from globl import *
from data import *
from network import Dispatcher
from network import Protocol

class TransactionDispatcher(Dispatcher):
	def transaction(self, tId, time, value, giverId, receiverId, privateKey):
		print(
			'Incoming transaction\n'
			'TID:\t\t%d\n'
			'Time:\t\t%d\n'
			'Value:\t\t%.2f\n'
			'Giver:\t\t%d\n'
			'Receiver\t%d\n'
			% (tId, time, value, giverId, receiverId))
		
		# Retrieves and update peers balance
		giver = find(PATH['PEERS'], giverId)
		receiver = find(PATH['PEERS'], receiverId)
		receiver.balance += value
		giver.balance -= value

		# Creates a new transaction object
		tx = Transaction()
		tx.id = tId
		tx.time = time
		tx.value = value
		tx.giver = giver
		tx.receiver = receiver
	
		# Save own transaction
		if giverId == WHO_I_AM:
			save(PATH['TX_MINE'], tx)

		if checkPeerKey(giver, privateKey) and giver.balance - value >= 0:
			# Transaction has been approved
			# Persists transaction on temporary file
			save(PATH['TX_TEMP'], tx)

			# Sends a positive acknowledgment
			print('Transaction approved\nTID:\t\t%d\n' % (tId))
			self.ack(tId, WHO_I_AM, True)
		else:
			# Sends a negative acknowledgment in case of disapproval
			print('Transaction disapproved\nTID:\t\t%d\n' % (tId))
			self.ack(tId, WHO_I_AM, False)

	def ack(self, tId, peerId, approved):
		tx = find(PATH['TX_MINE'], tId)

		if tx is None:
			# Transaction is not mine
			# Send acknowledgement to previous peer
			prev = Protocol(NET_GROUP['PREV'])
			prev.sendParams('ack', tId, peerId, approved)
			prev.close()
		else:
			# Transaction is mine
			# Add acknowledgement to the proper ack group
			handler = AckHandler(PATH['ACKS'], tId)
			handler.add(peerId, approved)

			print(
				'Acknowledgement received\n'
				'TID:\t\t%d\n'
				'From:\t\t%d\n'
				'Remaining:\t%d/%d\n'
				% (tId, peerId, handler.count, PEERS_COUNT))

			# If every peer sent their acknowledgements
			if handler.count == PEERS_COUNT:
				remove(PATH['TX_MINE'], tId)
				approved = handler.approved == ACKS_TO_APPROVE
				
				# Removes acknowledgements that are no longer needed
				handler.clear()

				# Sends commit to everyone
				self.chaining(('commit', tId, approved))

	def commit(self, tId, approved):
		tx = remove(PATH['TX_TEMP'], tId)

		if tx != None and approved:
			# Save all changes
			save(PATH['TX_COMMIT'], tx)
			save(PATH['PEERS'], tx.giver)
			save(PATH['PEERS'], tx.receiver)

		print(
			'Transaction completed\n'
			'TID:\t\t%d\n'
			'Status:\t\t%s'
			% (tId, 'success' if approved else 'unsuccessfully'))

	def chaining(self, params, counter = 0, direction = 'NEXT'):
		counter += 1
		self.execute(params)

		if counter < PEERS_COUNT:
			proto = Protocol(NET_GROUP[direction])
			proto.sendParams('chaining', params, counter, direction)
			proto.close()

from itertools import chain, combinations, permutations


# example for the required format for buyers and sellers
BUYERS = [
			['2$', '3mbps', 'B'], 
			['2$', '3mbps', 'A'],
			['5$', '3mbps', 'B']
			]

SELLERS = [
			['0.5$', '4mbps', set(['B'])],
			['0.5$', '3mbps', set(['B'])],
			['0.5$', '2mbps', set(['A','B'])]
			]


class SwarmVCG(object):


	@staticmethod
	def subsets(arr):
	    """ Note this only returns non empty subsets of arr"""
	    return chain(*[combinations(arr,i + 1) for i,a in enumerate(arr)])

	@staticmethod
	def k_subset(arr, k):
	    s_arr = sorted(arr)
	    return set([i for i in combinations(SwarmVCG.subsets(arr),k) 
	               if sorted(chain(*i)) == s_arr])

	@staticmethod
	def reformat_buyers(buyers_list):
		return [[float(i[0][:-1]), int(i[1][:-4]), i[2]] for i in buyers_list]

	@staticmethod
	def reformat_sellers(sellers_list):
		return [[float(i[0][:-1]), int(i[1][:-4]), i[2]] for i in sellers_list]

	@staticmethod
	def generate_products(sellers_list):
		products = []
		for seller_ind in range(len(sellers_list)):
			capacity = sellers_list[seller_ind][1]
			for cap in range(capacity):
				products.append(seller_ind)

		return products


	def __init__(self, buyers, sellers):
		self.buyers = self.reformat_buyers(buyers)
		self.sellers = self.reformat_sellers(sellers)
		self.products = self.generate_products(self.sellers)


	def evaluate(self, buyer, product_set):
		buyer_capacity = buyer[1]
		buyer_payment = buyer[0]
		buyer_looking_for = buyer[2]
		valuation = 0
		for prod_ind in product_set:
			if buyer_capacity == 0:
				break
			if buyer_payment < self.sellers[prod_ind][0]:
				# the buyer will never buy it, so there's no point to evaluate it in
				continue
			if buyer_looking_for in self.sellers[prod_ind][2]:
				valuation += buyer_payment
				buyer_capacity = buyer_capacity - 1

		return valuation


	def find_maximizing_set(self, buyers):
		all_partitions = self.k_subset(self.products,len(buyers))
		max_sum_partition = 0
		max_partition_set = []
		for partition in all_partitions:
			for partition_perm in permutations(partition):
				sum_partition = 0
				for partition_part_ind in range(len(partition_perm)):
					sum_partition += self.evaluate(buyers[partition_part_ind], partition_perm[partition_part_ind])
				if sum_partition > max_sum_partition:
					max_sum_partition = sum_partition
					max_partition_set = partition_perm

		return max_sum_partition, max_partition_set

	def compute(self):
		matching_set_sum, matching_set = self.find_maximizing_set(self.buyers)
		print("MATCHING SET: {}".format(matching_set))
		buyer_prices = []
		final_matching_set = []
		for buyer_ind in range(len(self.buyers)):
			no_buyer_sum, _ = self.find_maximizing_set(self.buyers[:buyer_ind] + self.buyers[buyer_ind + 1:])
			externalities_price = no_buyer_sum - matching_set_sum + self.evaluate(self.buyers[buyer_ind], matching_set[buyer_ind])
			reserve_based_price = 0
			matching_set_for_buyer = []
			for prod_ind in matching_set[buyer_ind]:
				reserve_price = self.sellers[prod_ind][0]
				buyers_payment = self.buyers[buyer_ind][0]
				buyer_looking_for = self.buyers[buyer_ind][2]
				if buyers_payment > reserve_price and buyer_looking_for in self.sellers[prod_ind][2]:
					reserve_based_price += reserve_price
					matching_set_for_buyer.append(prod_ind)
			buyer_prices.append(max([reserve_based_price, externalities_price]))
			final_matching_set.append(matching_set_for_buyer)

		print("FINAL MATCHING SET: {}".format(final_matching_set))
		print("BUYER PRICES: {}".format(buyer_prices))

		return final_matching_set, buyer_prices

#SwarmVCG(BUYERS,SELLERS).compute()



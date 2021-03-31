# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 08:42:40 2021

@author: Claudio Borgini
"""

import re # module for RegEx

from money import Money


def extract_quantity_price_tax_adtax(input_string):

    
    n_receipt = 1                           # counter for receipts output
    
    for index in (input_string):            # computes every list of items
        
        total_price = 0.000                 # sum of item's prices
        total_tax = 0.000                   # sum of item's taxes

        quantity_item_price_list = []       # list used to memorize calculations to print on receipt
        
        for element in index:               # group of component of one row in the list using RegEx
            risultato=re.search(r'(\d{1,}\s*)((\w*\s*){1,})([a][t]\s*)(\d{1,}[\.]\d{1,})', element)

            q = int(risultato.group(1))     # quantity
            t = risultato.group(2)          # item
            p = float(risultato.group(5))

            quantity_item_price_list.append(q)  # [0] quantity 
            quantity_item_price_list.append(t)  # [1] item
            
            tax, adtax = get_taxes(t)

            price_list = (q * p) + (q * p * (tax+adtax)) 
            ###print("prezzo:", price_list)
            quantity_item_price_list.append(price_list) # [2] total_price+taxes
            total_price = total_price + price_list

            quantity_item_price_list.append(tax)        # [3] tax
            quantity_item_price_list.append(adtax)      # [4] adtax
            
            quantity_item_price_list.append(q * p)      # [5] price before taxes
            
            ###print(quantity_item_price_list) # debug print, after debug comment this
        
        print_receipt(n_receipt, quantity_item_price_list)
        n_receipt+=1            


            
def get_taxes(item):
    
    
    'set containing no tax goods'
    no_tax = {"book", "box", "bar", "headache", "chocolate", "chocolates", "pill", "pills", "packet"}
    ###print("esenzione per ", no_tax)
    
    #print("tasse per: ", item)
    
    item_part = item.split()
    #print("componenti: ", item_part)

    adtax = 0.000
    #adtax_b = False
    
    #print("item:", item)
    if "imported" in item:
        adtax = 0.050
        item = item.replace('imported', '')
    else:
        adtax = 0.000
    #print("AdTax: ", adtax)
    

    
    tax = 0.000
    tax_b = False

    #print("tasse per: ", item)
    
    item_part = item.split()
    #print("componenti: ", item_part)

    for x in item_part:
        if x in no_tax:
    #         print("no tax")
             tax_b = tax_b + False
             break
        else:
    #         print("tax")
             tax_b = tax_b + True
             

    if tax_b:
        tax = 0.100
    #print("Tax: ", tax)
 
        
    
    return tax, adtax
    


def print_receipt(n, quantity):
    sales_taxes = 0
    total = 0
    
    print("Output :", n)

    for i in range(0, len(quantity),6):
        sales_taxes = sales_taxes + (float(quantity[i+2])-float(quantity[i+5]))
        ###print("Total, total-no-tax: ",float(quantity[i+2]), float(quantity[i+5]))
        total = total + float(quantity[i+2])
        
        print(quantity[i], quantity[i+1], ":", Money(float(quantity[i+2]), "EUR")) 

    print("Sales Taxes: ", Money(sales_taxes, "EUR"))
    #print(total)
    total = Money(total, "EUR")
    
    print("Total: ", total)
    print()
    print("---------------------")
    print()
    
        
def main():
    
    # list of tuples contaning sample strings
    input_1 = [("2 book at 12.49", "1 music CD at 14.99", "1 chocolate bar at 0.85"), ("1 imported box of chocolates at 10.00", "1 imported bottle of perfume at 47.50"), ("1 imported bottle of perfume at 27.99", "1 bottle of perfume at 18.99", "1 packet of headache pills at 9.75", "3 box of imported chocolates at 11.25")]
    
    extract_quantity_price_tax_adtax(input_1) 
    
    
    
main()

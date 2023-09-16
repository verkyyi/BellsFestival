import re
s='''
*Status:
   This page was built from the database on  8-May-18
   based on textual data last updated on 2018/05/07
   and on technical data last updated on 2018/05/07
------------------------------

------------------------------
*Location:   St.Thaddeus Episcopal Church
   Pendleton Street SW
     at Augusta-Aiken Road (US Hwy 1)
   Aiken, South Carolina, USA
   LL: N 33.56190, W 81.72463
------------------------------
*Carillonist:   Donald Dupee, Director of Music
   T: (803)648-7662
   E: don@stthaddeus.org
   ------------------------------
*Past carillonist:
   19??-?? R.B.McKellar   (d.)
'''
def func():
   lines = s.splitlines()
   for i,line in enumerate(lines):
      if line[-3:]=="USA": 
         print("address here1")
         print(lines[:i])
         print("address here2")
         adress=''.join(lines[:i])
         print(adress)
         return(adress)

   


# Define a regular expression pattern to match latitude and longitude
pattern = r'LL:\s*N (\d+\.\d+),\s*W (\d+\.\d+)'

# Use re.search to find the pattern in the text
match = re.search(pattern, s)

# Check if a match was found
if match:
    # Extract and print latitude and longitude
    latitude = match.group(1)
    longitude = match.group(2)
    print("Latitude:", latitude)
    print("Longitude:", longitude)
else:
    print("Latitude and longitude not found.")


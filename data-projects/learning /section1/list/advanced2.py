# fix this code so that it prints a sorted list of all of our friends (alphabetical). Scroll to see answer 

friends = ['Simon', 'Patty', 'Joy', 'Carrie', 'Amira', 'Chu']
new_friend = ['Stanley']

# solution:

friends.extend(new_friend)
print(sorted(friends))

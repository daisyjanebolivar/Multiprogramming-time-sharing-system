import random
import time
import os

resources = []

class Resource:
  def __init__(self, name):
    self.name = name
    self.status = True  # default: currently in use
    self.queue = []  # list of users requesting the resource
    self.curr_user = None

  def display_next(self):
    print(self.name.upper())
    if not self.queue:
      print("\033[92mEmpty\033[0m")
    else:
      print("\033[93m"+str(self.queue[0].get_name()) + " ({:02d}s)".format(self.queue[0].get_time(self))+"\033[0m")

  def get_user(self):  # iterate thru queue
    if self.curr_user: # user currently using resource
      return self.curr_user
    for i in range(len(self.queue)):
      curr = self.queue[i]
      if not curr.status:  # user is free
        return curr
    return None

  def set_curr_user(self, user):
    self.curr_user = user
    if not user.curr_status(): # not busy
      user.change_status() # set to true aka user is now busy
    if user in self.queue:
      self.queue.remove(user)

  def change_status(self):
    if self.status:
      self.status = False
    else:
      self.status = True

class User:
  def __init__(self, name, res):
    self.name = name
    self.status = False  # is user currently using a resource?
    self.res = res

  def get_name(self) -> str:
    return self.name

  def get_time(self, key) -> int:
    return self.res.get(key)

  def change_status(self):
    if self.status:
      self.status = False
    else:
      self.status = True

  def curr_status(self) -> bool:
    return self.status

  def countdown(self, resource):
    self.res[resource] -= 1

# generate resources
num_of_resources = random.randint(1,30)
res_names = []
for i in range(num_of_resources):  # generates random resource names
  res_name = random.randint(1, 30)
  if res_name not in res_names:  # checks duplicates
    res_names.append(res_name)
  else:
    i -= 1
res_names.sort()
for x in res_names:  #generates a list of resources
  item = Resource("Resource {:02d}".format(x))
  resources.append(item)

# generates unique resource list for every user
def create_res_list():
  copy_res = resources.copy()
  user_res = random.randint(0,num_of_resources)  # num of resources for a user
  if user_res > 0:
    res_times = {}
    keys = random.choices(copy_res)
    for i in keys:
      res_times[i] = random.randint(1, 30)  # time
    return res_times
  else:
    return {}  # return empty dict; no requests

# searches for resource in a specific user's resource list
# if found, user is added to that resource's queue
def add_to_res_queue(user: User):
  for x in resources:
    if x in user.res:
      x.queue.append(user)

# generates users
def generate_users():
  num_of_users = random.randint(1, 30)
  user_nums = []
  for i in range(num_of_users):  # generates random user numbers
    user_num = random.randint(1, 30)
    if user_num not in user_nums:  # checks duplicates
      user_nums.append(user_num)
    else:
      i -= 1
  user_nums.sort()
  for x in user_nums:
    name = "User {:02d}".format(x)
    curr = User(name, create_res_list())
    add_to_res_queue(curr)


def all_free(resources):  # check if all resources are in use or not
  for x in resources:
    if x.status:  # resource is still being used
      return False
  return True  # all resources are free

def main():
  generate_users()
  while not all_free(resources):
    os.system('clear')
    for resource in resources:
      if not resource.queue and not resource.curr_user:  # empty queue and curr_user is already done
        if resource.status: # resource status still in use
          resource.change_status()
        print(resource.name +
              "                \033[92mFREE\033[0m                       ")
      else:
        user = resource.get_user()
        if not user:  # no available users
          print(resource.name + "                \033[93mIDLE\033[0m                    ")
        else:
          resource.set_curr_user(user)  #change status to true and pop from queue
          user_time = user.get_time(resource)
          if user_time < 0:
            print(str(resource.name))
            user.change_status() # change to false
            resource.curr_user = None # reset curr user
          else:
            print(str(resource.name) + ' \t' + user.name +
              ' \tTime: {:02d}s'.format(user_time))
            user.countdown(resource)
    print("--------------------------------------")
    print("\033[1m\033[96m  WAITLIST \033[0m")
    for r in resources:
      r.display_next()

    time.sleep(1)

if __name__ == "__main__":
    main()

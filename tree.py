# why not make a piece of code that automatically sorts order in which methods appear to up builtin methods towards the top and group methods that reference each other together?
import weakref
import json
try:
    import cPickle as pickle
except ModuleNotFoundError:
    import pickle

#template function for the 'Find' function in the General XP (GXP) Class
def recursive_find(target, origin):
  if origin.name == target:
    return origin
  for new_origin in origin.boys:
    #print(new_origin.name, origin.name)
    result = recursive_find(target, new_origin)
    if result == None:
      continue
    else:
      return result

#Enables the hierarchical and 'forward propagating' tree format that experience points are stored in
class GXP():
  def __init__(self, name, xp, parent=None):
    self.name = name
    self.xp = xp
    self.cached_xp = xp
    self.boys = []
    self.parent = parent
    self.level = (lambda x: x.level+1 if x != None else 0)(self.parent) #finds which hierarchical level the node/leaf is on upon creation by counting parents/earlier nodes
    print('initiated node at level:', self.level, ', name:',self.name)

  # returns a list of all nodes in the tree 'cumulative boys'
  def __getitem__(self, index):
    return self.get_cum_boys(self)[index]

  def __del__(self): 
    print('node', self.name, 'worth', self.xp,'destroyed')
    self.cached_xp = 0
    self.linear_update()
    print()

  #obsolete function previously ensuring proper deletion of node and its child nodes
  def delete(self):
    for i in self.parent.boys:
      if i.name == self.name:
        self.parent.boys.remove(i)
    # self.cached_xp = 0
    # self.linear_update()
    # self.parent = None
    # print('running')

  #finds a particular node by name
  def find(self, target):
    if self.name == target:
      return self
    for new_self in self.boys:
      #print(new_origin.name, origin.name)
      result = new_self.find(target)
      if result == None:
        continue
      else:
        return result
    
  #obtain references to all nodes in tree 
  def get_cum_boys(self, origin): #the origin argument is an appendix and has no function
    cum_boys = [self]
    for i in self.boys:
      result = i.get_cum_boys(origin)
      cum_boys = cum_boys + result
    return cum_boys
    #print('process_2_of', self.name)
    #print([i.name for i in cum_boys])
    # cum_boys.append(self)
    # cum_results = []
    # for i in self.boys:
    #   print(i.name)
    #   result = i.get_cum_boys(origin, cum_boys=cum_boys)
    #   print('result', result)
    #   cum_results = cum_results + result
    #   # if self.name == origin.name:
    #   #   continue
    #   # else:
    #   #   return cum_boys
        
    # if self.name == origin.name:
    #   return result
    # if self.boys == None:
    #   return cum_boys
    # return cum_results
    
  #returns sorted cumulative_boys
  def sorted(self, key=lambda x: x.name):
    return sorted(self.get_cum_boys(self), key=key)
    
  def update_xp(self, new_xp):
    self.cached_xp = self.cached_xp + new_xp - self.xp
    self.xp = new_xp
    self.linear_update()

  # creates a child of the current node. This also returns the child so you can call the method again to create a child of the child you just created. Allows multiple nodes to be created simultaneously
  def insert(self, *nodes):
    for name, data in nodes:
      # print('test',weakref.ref(self)())
      self.boys.append(GXP(name, data, weakref.proxy(self)))
      boy = self.boys[-1]
      boy.linear_update()
    self.boys.sort(key = lambda x: x.name)
    return boy #does boy equal to the boy appended in the list: yes 

  #recalculate cached xp
  def get_stacked_xp(self):
    boy_xp = self.xp
    for boy in self.boys:
      boy_xp += boy.get_stacked_xp()
    self.cached_xp = boy_xp
    return self.cached_xp

  #get currently stored cached xp
  def get_cached_xp(self, insure=False):
    if insure == True:
      self.get_stacked_xp()
    return self.cached_xp

  #recalculates all cached xp above current node(towards the root)
  def linear_update(self):
    try:
      if self.parent == None:
        return
    except ReferenceError:
      return
    new_sum = [self.parent.xp]
    new_sum = new_sum + [i.cached_xp for i in self.parent.boys]
    self.parent.cached_xp = sum(new_sum)
    # print('linearly_propagating_from:', self.parent.name, ', total xps:', new_sum)
    # print(self.parent.boys)
    # print('current value of', self.parent.name ,self.parent.cached_xp, self.parent.xp)
    self.parent.linear_update()
    # print('linear updated')

  #changes experience of current node without replacing it, can add negative numbers
  def add_experience(self, xp):
    self.xp += xp
    self.cached_xp += xp
    self.linear_update()

  #save tree to json file for future retrieval
  def save(self):
    with open('tree_storage.json', 'w') as file:
      tree = {}
      for i in self.get_cum_boys(self)[1:]:
        # print(i.name)
        tree[i.name] = {'name':i.name, 'xp':i.xp, 'parent':i.parent.name}
      # print(tree)
      json.dump(tree,file)


#retrieve root
def load_json_tree():
  with open('tree_storage.json','r') as json_tree:
    tree = json.load(json_tree)
    Root = GXP('root', 0)
    for node in tree:
      name = tree[node]['name']
      xp = tree[node]['xp']
      parent = tree[node]['parent']
      Root.find(parent).insert((name,xp))
  return Root
def load_pickled_root():
  with open('pickle_file.pkl','rb') as pickled_root:
    return pickle.load(pickled_root)

def replacer(origin, text, index, length=None):
  if length == None:
    length = len(text)
  output = origin[:index] + text + origin[index+length:]
  return output

def txt_find_node_start(line):
  output = [0]
  for x,i in enumerate(line):
    if i == '_':
      output.append(x+1)
  # optional segment to output the the location in the middle of various node names
  # last = None
  # for x,i in enumerate(output):
  #   if last == None:
  #     last = i
  #     continue
  #   new_i = (last+i)//2
  #   # print(new_i, i, last)
  #   last = i
  #   output[x-1] = new_i
  output.pop()
  output = [i+2 for i in output]
  return output

def print_xp_tree(Root, gui_mode = False):
  output = []
  level_dict = {}
  for i in Root.get_cum_boys(Root):
    level_dict[i.level] = []
  for i in Root.get_cum_boys(Root):
    level_dict[i.level].append(i)
  # print(level_dict)
  for level, nodes in level_dict.items():
    line = '_'.join([i.name for i in nodes])+'_'
    # print(level, line)
    output.append('_'.join([str(level),line]))
    for j in range(0, len(nodes)+1):
      i_locations = txt_find_node_start(line)
      string_list = ['_' for i in range(i_locations[-1]+1)]
      string_list = ''.join(string_list)
      j = j-1 #extends or reduces up-down line length
      for i,l in enumerate(i_locations):
        if j == -1:
          string_list = replacer(string_list, str(nodes[i].cached_xp), l)
          pass
        if j <= len(nodes)-i-2 and j != -1:
          if gui_mode:
            continue
          string_list = replacer(string_list, '|', l)
        elif j == len(nodes)-i-1:
          if gui_mode:
            continue
          string_list = replacer(string_list, '├', l)
          # string_list[l] = '|' 
      #e_string = ''.join(string_list)
      e_string = string_list
      output.append(e_string)
      # print(e_string)
  return '\n'.join(output)



  
"""
├─┬┐
└┐││
│└┬┐
├┐││
"""


from database.DAO import DAO
from model.model import Model

res = DAO.getAllSighting()
state = DAO.getAllStates()
model = Model()

print(len(state))
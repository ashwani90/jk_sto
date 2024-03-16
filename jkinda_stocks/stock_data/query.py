from stock_data.models import CompanyDetails

def create_query(oper):
    all_ops = oper.split(":")
    query_ops = []
    for ops in all_ops:
        ops = ops.split(",")
        if len(ops)<3:
            continue
        query_ops.append({
            "key": ops[0],
            "operator": ops[1],
            "value": ops[2]
        })
    qb = QueryBuilder(query_ops, "CompanyDetails")
    
    result = qb.execute_query()
    data = []
    for res in result:
        data.append({
            "name": res.company.name,
            "id": res.company.id,
            "symbol": res.company.symbol,
            "face_value": res.face_value,
            "p_e": res.p_e,
            "market_cap": res.market_cap
        })
    return data

    
class QueryBuilder():
    
    OPERATORS = {
        "gt": ">",
        "lt": "<",
        "gte": ">=",
        "lte": "<=",
        "e": "=",
        "eq": "=",
        "ne": "<>"
    }
    
    def __init__(self, ops, model):
        self.ops = ops
        self.model = model
        self.query = ""
        
    def generate_query(self):
        if self.model == "CompanyDetails":
            self.query = "select * from stock_data_companydetails where "
            self.model = CompanyDetails
            
    def add_operators(self):
        for op in self.ops:
            key = op.get('key')
            operator = op.get('operator')
            value = op.get('value')
            self.query = self.query + key + " " + self.OPERATORS[operator] + " '" + value + "'"
        self.query = self.query + " LIMIT 10"
        
    def get_query(self):
        return self.query
    
    def execute_query(self):
        self.generate_query()
        self.add_operators()
        result = self.model.objects.raw(self.query)
        return result
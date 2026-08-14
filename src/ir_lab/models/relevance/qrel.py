from dataclasses import dataclass

@dataclass
class Qrel : 
  query_id : int 
  document_id : int 
  metadata : dict | None = None




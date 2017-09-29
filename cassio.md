#Issues

I downloaded Anaconda and made an environment using Python 3.6.0  

1. If you install an environment using 3.6.2, you can't install using `pip install cassiopeia` 

Solution: Make a new environment with 3.6.0, and run it
 
2. There was a problem with pycurl; something like 
` ImportError: pycurl: libcurl link-time version (7.37.1) is older than compile-time version (7.43.0)`

Solution: `conda install pycurl`  

3. Got an error with DiGraph having no attribute 'edge'  
Problem involved using `pip install cassiopeia` 

Solution: Use `pip install git+https://github.com/meraki-analytics/cassiopeia.git`  
Also use Python 3.6.0  

Gives this error:

```
(league) (xenial)aaron@localhost:~/Documents/morellonomicon$ python testcass2.py
Traceback (most recent call last):
  File "testcass2.py", line 5, in <module>
    cass.set_riot_api_key("RGAPI-d2b7bfdf-b2d8-49ca-9885-305c4ae13659")  # This overrides the value set in your configuration/settings file.
  File "/home/aaron/anaconda3/envs/league/lib/python3.6/site-packages/cassiopeia/cassiopeia.py", line 33, in set_riot_api_key
    configuration.settings.set_riot_api_key(key)
  File "/home/aaron/anaconda3/envs/league/lib/python3.6/site-packages/cassiopeia/_configuration/settings.py", line 111, in set_riot_api_key
    for sources in self.pipeline._sources:
  File "/home/aaron/anaconda3/envs/league/lib/python3.6/site-packages/cassiopeia/_configuration/settings.py", line 90, in pipeline
    self.__pipeline = create_pipeline(verbose=False, service_configs=self.__pipeline_args)
  File "/home/aaron/anaconda3/envs/league/lib/python3.6/site-packages/cassiopeia/_configuration/settings.py", line 35, in create_pipeline
    pipeline = DataPipeline(services, transformers)
  File "/home/aaron/.local/lib/python3.6/site-packages/datapipelines/pipelines.py", line 283, in __init__
    self._type_graph = _build_type_graph(sources, sinks, transformers)
  File "/home/aaron/.local/lib/python3.6/site-packages/datapipelines/pipelines.py", line 71, in _build_type_graph
    current_transformer = graph.edge[from_type][to_type][_TRANSFORMER]
AttributeError: 'DiGraph' object has no attribute 'edge'
``` 

4. Problem with championgg  

Solution: ????


```
(league) (xenial)aaron@localhost:~/Documents/morellonomicon$ python testcass.py
Traceback (most recent call last):
  File "testcass.py", line 35, in <module>
    get_champions()
  File "testcass.py", line 7, in get_champions
    annie = Champion(name="Annie", region="NA")
  File "/home/aaron/anaconda3/envs/league/lib/python3.6/site-packages/cassiopeia/core/common.py", line 41, in default_region_wrapper
    return method(self, *args, **kwargs)
  File "/home/aaron/anaconda3/envs/league/lib/python3.6/site-packages/cassiopeia/core/common.py", line 170, in __call__
    pipeline = configuration.settings.pipeline
  File "/home/aaron/anaconda3/envs/league/lib/python3.6/site-packages/cassiopeia/_configuration/settings.py", line 116, in pipeline
    self.__pipeline = create_pipeline(verbose=False, service_configs=self.__pipeline_args)
  File "/home/aaron/anaconda3/envs/league/lib/python3.6/site-packages/cassiopeia/_configuration/settings.py", line 27, in create_pipeline
    module = importlib.import_module(name=package)
  File "/home/aaron/anaconda3/envs/league/lib/python3.6/importlib/__init__.py", line 126, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
  File "<frozen importlib._bootstrap>", line 978, in _gcd_import
  File "<frozen importlib._bootstrap>", line 961, in _find_and_load
  File "<frozen importlib._bootstrap>", line 936, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 205, in _call_with_frames_removed
  File "<frozen importlib._bootstrap>", line 978, in _gcd_import
  File "<frozen importlib._bootstrap>", line 961, in _find_and_load
  File "<frozen importlib._bootstrap>", line 948, in _find_and_load_unlocked
ModuleNotFoundError: No module named 'championgg'
```

Solution: Remove 
`cass.set_riot_api_key("RGAPI-d2b7bfdf-b2d8-49ca-9885-305c4ae13659")`  
`cass.set_default_region("NA")`  

Use environment variables for API keys and region, use google if you don't know how to  

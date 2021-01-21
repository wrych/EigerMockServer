# EigerMockServer

This is a simple EIGER mock API Server intended for developing or testing BRUENIG EIGER client.

## Installation

Please note that the following modules are required or recommended to run the mock server. I strongly recommend setting up a virtual environment to run the server in. 

### Required Modules
```
flask, flask_cors
```
If you want to run the test, `pytest` is required.

### Recommended Modules
```
black
```

## Usage
You may run the EIGER mock server with the command

```
python Eiger.py
```


I considered putting BRUENIG and this mock server in one project, but decided against it. This server is meant for only a short live span. I recommend downloading BRUENIG into a seperate folder. You may execute `python -m http.server` in the BRUENIG directory. The python http server will serve BRUENIG on port 8000. The API will be running on port 5000 by default. You may change either of those ports if required.
Be aware that at least EIGER (Jaun) Versions below 1.8.x do not support CORS. You will either have to start the browser with reduced security settings or use an add-on like CORS Everywhere to be able to communicate to real detectors. The mock server provides CORS header by default and thus, you can run it on every browser.

You may download BRUENIG from following public repository:
```
https://github.com/wrych/BRUENIG.git
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
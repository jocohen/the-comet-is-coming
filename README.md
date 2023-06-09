# The Comet Is Coming

The comet is coming is a Django website that implements NASA Near Earth Object API
to display the asteroids approaching Earth between certain dates.

Works for Python v11, Django v4.2

## Requirements

This project requires the following:
- [Docker](https://docs.docker.com/get-docker/)

## Installation

1. Get your NASA API key at https://api.nasa.gov/index.html#signUp
2. Clone the repository and cd into it
3. Create .env file
   ```bash
   cp sample.env .env
   ```
4. Obtain a Django secret key : [here](https://utils.brntn.me/django-secret/)
5. Modify .env with your NASA API key and Django secret key to have something like this :
    ```env
    NASA_API_KEY=huih2138dxnfi29
    DJANGO_SECRET_KEY=$mf$ep=*eckul#^$87uo#&tp*3bu*wrre_-xu
    ```

## Usage

Use the makefile to up the container:
```bash
make up
```

Website hosted on http://0.0.0.0:8000

To see other makefile rules:
```bash
make
```

## Todo

- Possibility to have order_by on certain params on [CometsListView](app/comets/views/comets_list.py), [CometDetailView](app/comets/views/comet_detail.py)
- Have home UI display a comet when the comet is really coming
- Add a faker to test mapping of data in NASA service
- Deploy in production
- Clearer UI explanation
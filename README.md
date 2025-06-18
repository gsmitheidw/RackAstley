# RackAstley
Draw Server Room/Data Centre Racks diagrams in plain text from yaml or user input

## Instructions

1. clone repo
2. pip install -r requirements.txt (probably best in a venv)
3. (optional) create a rack layout yaml using template example
4. run python3 RackAstley.py


## Usage:

Rack items can be printed to clipboard/screen individually or you can define a rack in yaml.

For yaml import, a sample is provided. Each rack item has a name, a position (the U value it starts at)
and the height of that item. Gaps can be left for unfilled rack positions. Also there's a name for the 
rack and height in U of the whole rack (usually 42).  


### Sample yaml

```yaml
rack:
  name: Rack1
  height: 24
  devices:
    - name: UPS
      position: 1
      size: 2
    - name: Firewall
      position: 3
      size: 1
    - name: WebServer01
      position: 4
      size: 1
    - name: WebServer02
      position: 5
      size: 1
    - name: Switch
      position: 6
      size: 2
```

### Sample output:

```
[RACK Rack1]
[24] 
[23] 
[22] 
[21] 
[20] 
[19] 
[18] 
[17] 
[16] 
[15] 
[14] 
[13] 
[12] 
[11] 
[10] 
[09] 
[08] 
[07] ┌───Switch──────────{2U}─┐
[06] └────────────────────────┘
[05]〘====WebServer02===={1U}═〙
[04]〘====WebServer01===={1U}═〙
[03]〘=====Firewall======{1U}═〙
[02] ┌───UPS─────────────{2U}─┐
[01] └────────────────────────┘
```

### Notes:

- Double width characters used for 2 ends of 1U units, if you wish to change this you'll have to edit the code to allow for single width character after the rack position.
- Box drawing characters are used for any items 2U and larger.




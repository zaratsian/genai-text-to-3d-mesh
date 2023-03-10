# Copyright 2023 Google LLC All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

'''
This is a sample script that can be used to make a call to the Text to 3d model 
that has been deployed using the code within this repo. 
'''

import open3d as o3d # open3d==0.16.1
import numpy as np
import requests

host = 'localhost'
port = 8501
text = 'mountain bike'


# Make a REST POST requests to the Model Endpoint (that is deployed in GKE)
response = requests.post('http://localhost:8501/tt3d', json={'text':text})

# Save the response as a mesh file.
with open('mesh.ply', 'wb') as f:
    f.write(response.content)

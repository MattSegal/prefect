---
sidebarDepth: 2
editLink: false
---
# Base Environments
---
 ## LocalEnvironment
 <div class='class-sig' id='prefect-environments-local-localenvironment'><p class="prefect-sig">class </p><p class="prefect-class">prefect.environments.local.LocalEnvironment</p>(encryption_key=None, serialized_flow=None)<span class="source"><a href="https://github.com/PrefectHQ/prefect/blob/master/src/prefect/environments/local.py#L11">[source]</a></span></div>

LocalEnvironment is an encrypted and serializable environment for simply packaging up flows so they can be stored and transported.

**Args**:     <ul class="args"><li class="args">`encryption_key (bytes)`: key to use in serialization or deserialization of the environment     </li><li class="args">`serialized_flow (bytes)`: a Prefect Flow object that is serialized</li></ul>

|methods: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|
|:----|
 | <div class='method-sig' id='prefect-environments-local-localenvironment-build'><p class="prefect-class">prefect.environments.local.LocalEnvironment.build</p>(flow)<span class="source"><a href="https://github.com/PrefectHQ/prefect/blob/master/src/prefect/environments/local.py#L33">[source]</a></span></div>
<p class="methods">Build the LocalEnvironment. Returns a LocalEnvironment with a serialized flow attribute.<br><br>**Args**:     <ul class="args"><li class="args">`flow (Flow)`: The prefect Flow object to build the environment for</li></ul>**Returns**:     <ul class="args"><li class="args">`LocalEnvironment`: a LocalEnvironment with a serialized flow attribute</li></ul></p>|
 | <div class='method-sig' id='prefect-environments-local-localenvironment-deserialize-flow-from-bytes'><p class="prefect-class">prefect.environments.local.LocalEnvironment.deserialize_flow_from_bytes</p>(serialized_flow)<span class="source"><a href="https://github.com/PrefectHQ/prefect/blob/master/src/prefect/environments/local.py#L63">[source]</a></span></div>
<p class="methods">Deserializes a Flow to binary.<br><br>**Args**:     <ul class="args"><li class="args">`serialized_flow (bytes)`: the Flow to deserialize</li></ul>**Returns**:     <ul class="args"><li class="args">`Flow`: the deserialized Flow</li></ul></p>|
 | <div class='method-sig' id='prefect-environments-local-localenvironment-run'><p class="prefect-class">prefect.environments.local.LocalEnvironment.run</p>(runner_kwargs=None)<span class="source"><a href="https://github.com/PrefectHQ/prefect/blob/master/src/prefect/environments/local.py#L78">[source]</a></span></div>
<p class="methods">Runs the `Flow` represented by this environment.<br><br>**Args**:     <ul class="args"><li class="args">`runner_kwargs (dict)`: Any arguments for `FlowRunner.run()`.</li></ul>**Returns**:     <ul class="args"><li class="args">`State`: the state from the flow run</li></ul></p>|
 | <div class='method-sig' id='prefect-environments-local-localenvironment-serialize-flow-to-bytes'><p class="prefect-class">prefect.environments.local.LocalEnvironment.serialize_flow_to_bytes</p>(flow)<span class="source"><a href="https://github.com/PrefectHQ/prefect/blob/master/src/prefect/environments/local.py#L48">[source]</a></span></div>
<p class="methods">Serializes a Flow to binary.<br><br>**Args**:     <ul class="args"><li class="args">`flow (Flow)`: the Flow to serialize</li></ul>**Returns**:     <ul class="args"><li class="args">`bytes`: the serialized Flow</li></ul></p>|

---
<br>

 ## DockerEnvironment
 <div class='class-sig' id='prefect-environments-docker-dockerenvironment'><p class="prefect-sig">class </p><p class="prefect-class">prefect.environments.docker.DockerEnvironment</p>(base_image, registry_url=None, python_dependencies=None, image_name=None, image_tag=None, env_vars=None, files=None)<span class="source"><a href="https://github.com/PrefectHQ/prefect/blob/master/src/prefect/environments/docker.py#L18">[source]</a></span></div>

This is a base environment which takes a flow, serializes it into a LocalEnvironment, and places it inside of a Docker image. This image is then used in any environment which depends on using Docker containers (e.g. the Kubernetes environments).

**Args**:     <ul class="args"><li class="args">`base_image (string)`: the base image for this environment (e.g. `python:3.6`)     </li><li class="args">`registry_url (string, optional)`: URL of a registry to push the image to; image will not be pushed if not provided     </li><li class="args">`python_dependencies (List[str], optional)`: list of pip installable dependencies for the image     </li><li class="args">`image_name (string, optional)`: name of the image to use when building, defaults to a UUID     </li><li class="args">`image_tag (string, optional)`: tag of the image to use when building, defaults to a UUID     </li><li class="args">`env_vars (dict, optional)`: a dictionary of environment variables to use when building     </li><li class="args">`files (dict, optional)`: a dictionary of files to copy into the image when building</li></ul>

|methods: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|
|:----|
 | <div class='method-sig' id='prefect-environments-docker-dockerenvironment-build'><p class="prefect-class">prefect.environments.docker.DockerEnvironment.build</p>(flow, push=True)<span class="source"><a href="https://github.com/PrefectHQ/prefect/blob/master/src/prefect/environments/docker.py#L73">[source]</a></span></div>
<p class="methods">Build the Docker image. Returns a DockerEnvironment with the appropriate image_name and image_tag set.<br><br>**Args**:     <ul class="args"><li class="args">`flow (prefect.Flow)`: Flow to be placed the image     </li><li class="args">`push (bool)`: Whether or not to push to registry after build</li></ul>**Returns**:     <ul class="args"><li class="args">`DockerEnvironment`: a DockerEnvironment that represents the provided flow.</li></ul></p>|
 | <div class='method-sig' id='prefect-environments-docker-dockerenvironment-build-image'><p class="prefect-class">prefect.environments.docker.DockerEnvironment.build_image</p>(flow, push=True)<span class="source"><a href="https://github.com/PrefectHQ/prefect/blob/master/src/prefect/environments/docker.py#L97">[source]</a></span></div>
<p class="methods">Build the Docker image using the docker python library. Optionally pushes the image if both `push`=`True` and `self.registry_url` is set.<br><br>**Args**:     <ul class="args"><li class="args">`flow (prefect.Flow)`: Flow to be placed the image     </li><li class="args">`push (bool)`: Whether or not to push to registry after build</li></ul>**Returns**:     <ul class="args"><li class="args">`tuple`: `image_name`, `image_tag` (strings)</li></ul></p>|
 | <div class='method-sig' id='prefect-environments-docker-dockerenvironment-create-dockerfile'><p class="prefect-class">prefect.environments.docker.DockerEnvironment.create_dockerfile</p>(flow, directory=None)<span class="source"><a href="https://github.com/PrefectHQ/prefect/blob/master/src/prefect/environments/docker.py#L181">[source]</a></span></div>
<p class="methods">Creates a dockerfile to use as the container.<br><br>In order for the docker python library to build a container it needs a Dockerfile that it can use to define the container. This function takes the image and python_dependencies then writes them to a file called Dockerfile.<br><br>*Note*: if `files` are added to this container, they will be copied to this directory as well.<br><br>**Args**:     <ul class="args"><li class="args">`flow (Flow)`: the flow that the container will run     </li><li class="args">`directory (str, optional)`: A directory where the Dockerfile will be created,         if no directory is specified is will be created in the current working directory</li></ul></p>|
 | <div class='method-sig' id='prefect-environments-docker-dockerenvironment-pull-image'><p class="prefect-class">prefect.environments.docker.DockerEnvironment.pull_image</p>()<span class="source"><a href="https://github.com/PrefectHQ/prefect/blob/master/src/prefect/environments/docker.py#L149">[source]</a></span></div>
<p class="methods">Pull the image specified so it can be built.<br><br>In order for the docker python library to use a base image it must be pulled from either the main docker registry or a separate registry that must be set as `registry_url` on this class.</p>|
 | <div class='method-sig' id='prefect-environments-docker-dockerenvironment-push-image'><p class="prefect-class">prefect.environments.docker.DockerEnvironment.push_image</p>(image_name, image_tag)<span class="source"><a href="https://github.com/PrefectHQ/prefect/blob/master/src/prefect/environments/docker.py#L164">[source]</a></span></div>
<p class="methods">Push this environment to a registry<br><br>**Args**:     <ul class="args"><li class="args">`image_name (str)`: Name for the image     </li><li class="args">`image_tag (str)`: Tag for the image</li></ul></p>|

---
<br>


<p class="auto-gen">This documentation was auto-generated from commit <a href='https://github.com/PrefectHQ/prefect/commit/n/a'>n/a</a> </br>by Prefect 0.5.1+0.g71829f4e.dirty on April 4, 2019 at 23:56 UTC</p>
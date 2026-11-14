import cairnml_agent.glue.k8s as k8s
from cairnml_agent.glue import utilities as glue_utilities


def test_k8s_glue_uses_glue_utilities_get_bash_output():
    assert k8s.get_bash_output is glue_utilities.get_bash_output


def test_k8s_glue_get_bash_output_drops_stderr():
    cmd = "echo 'Warning: policy/v1beta1 is deprecated' >&2; echo 'pod-a value'"
    out = k8s.stringify_bash_output(k8s.get_bash_output(cmd)).splitlines()
    assert out == ["pod-a value"]

from prefect import flow, task


@task
def hello():
    return "BR381 pipeline iniciado"


@flow(name="br381-test-flow")
def br381_flow():

    result = hello()

    print(result)


if __name__ == "__main__":
    br381_flow()

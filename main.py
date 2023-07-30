import logging
# These modules provide the functionality to interact with a MySQL database and an OpenAI language model.
from langchain import OpenAI, SQLDatabase, SQLDatabaseChain

logger = logging.getLogger(__name__)


def main():
    #  creates a SQLDatabase object from the URI of the MySQL database
    db = SQLDatabase.from_uri("mysql+pymysql://root:shubh@localhost/cyb_ipl")
    # creates an OpenAI object with the text-davinci-003 model
    llm = OpenAI(model_name="text-davinci-003", temperature=0.7, verbose=True)
    #  used to interact with the database using the OpenAI language model.
    db_chain = SQLDatabaseChain.from_llm(llm, db,
                                     verbose=True,
                                     use_query_checker=True)
# The while True loop continuously prompts the user for input
    while True:
        user_input = input(
            """You can now chat with your database.
            Please enter your question or type 'quit' to exit: """
        )
        if user_input.lower() == 'quit':
            break

        try:
            response = db_chain.run(user_input)
        except Exception as e:
            if isinstance(e, mysql.connector.Error):
                logger.error(e)
                print("Error connecting to MySQL: {}.".format(e))
                continue
            else:
                raise

        print(response)


if __name__ == "__main__":
    main()

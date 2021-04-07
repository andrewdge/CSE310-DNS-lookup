import datetime
import sys
import dns.message
import dns.query


# Andrew Ge 170109055

# use: python cse310hw1.py mydig *ADDRESS*

def mydig(address, nameserver="198.41.0.4"):
    # f = open("output.txt", "a")
    # f.write("-----------------------------\n")

    # get query time
    startTime = datetime.datetime.now()
    # save root, original domain
    root = nameserver
    originDomain = address

    # keep trying until I find an answer
    while True:
        # print("-----------------------------------------")
        # print("ORIGIN DOMAIN: " + originDomain + "   SEARCH DOMAIN: " + address + "    NAMESERVER: " + nameserver)

        # create address query, look for A record
        queryMsg = dns.message.make_query(address, dns.rdatatype.A)
        # 198.41.0.4 is Root server IPV4 a.something

        # query using the message created. start from randomly chosen root ip
        resp = dns.query.udp(queryMsg, nameserver)
        # print(resp)

        # if we find an answer while searching for the original input, we're done
        if len(resp.answer) > 0 and originDomain == address:
            print("QUESTION SECTION:")
            print(resp.question[0])
            print("ANSWER SECTION:")
            print(resp.answer[0])
            # f.write("QUESTION SECTION:\n")
            # f.write(str(resp.question[0]) + "\n")
            # f.write("ANSWER SECTION:\n")
            # f.write(str(resp.answer[0]) + "\n")
            break
        # if we find an answer but we are using a sub address, try searching the original input on this new nameserver
        elif len(resp.answer) > 0 and originDomain != address:
            address = originDomain
            nameserver = str(resp.answer[0][0])
        # if no answer, but we find an additional, use the first A record IP
        elif len(resp.additional) > 0:
            for i in range(len(resp.additional)):
                if dns.rdatatype.to_text(resp.additional[i][0].rdtype) == "A":
                    nameserver = str(resp.additional[i][0])
        # if nothing in answer or additional, try searching for the first thing in authority
        elif len(resp.authority) > 0:
            address = str(resp.authority[0][0])
        # if nothing at all, try searching for the current nameserver on root ip
        else:
            nameserver = root

    # getting the query time, formatting
    endTime = datetime.datetime.now()
    elapsedTime = (endTime - startTime)
    print("Query Time: " + str(elapsedTime.total_seconds()) + " seconds")
    print("WHEN: " + startTime.date().strftime("%B %d, %Y") + " " + startTime.time().strftime("%I:%M:%S %p"))
    # f.write(str(elapsedTime.total_seconds())+"\n")
    # f.write("WHEN: " + startTime.date().strftime("%B %d, %Y") + " " + startTime.time().strftime("%I:%M:%S %p")+"\n")
    # f.close()


if __name__ == "__main__":
    # to run from cmdline
    globals()[sys.argv[1]](sys.argv[2])

    # f = open("output.txt", "w")
    # f.write("")
    # for i in range(10):
    #     mydig("www.instagram.com", nameserver="8.8.8.8")

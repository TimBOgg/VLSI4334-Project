import itertools

class QuinMcAlgo:
    def __init__(self, num_vars):
        self.num_vars = num_vars

    def parse_pla(self, filename):
        """
        Parses the input PLA file and separates its components.
        :param filename: The path to the PLA file to parse.
        :return: A tuple containing the header information and the minterms.
        """
        with open(filename, 'r') as file:
            lines = file.readlines()
        
        header = [line.strip() for line in lines if line.startswith(".")]
        body = [line.strip() for line in lines if not line.startswith(".") and line.strip() != ""]
        
        minterms = []
        for line in body:
            binary, output = line.split(" ")
            if output == "1":
                minterms.append(binary)
                print(binary)
        
        return header, minterms

    def minimize(self, minterms):
        """
        Minimizes the logic represented by the minterms using the Quine-McCluskey algorithm.
        :param minterms: A list of binary strings representing the minterms.
        :return: A list of minimized terms (prime implicants).
        """
        groups = self.group_by_ones(minterms)
        unchecked = set(minterms)
        checked = set()
        prime_implicants = set()

        while groups:
            next_groups = {}
            used = set()

            group_keys = sorted(groups.keys())
            for g1, g2 in zip(group_keys, group_keys[1:]):
                for term1 in groups[g1]:
                    for term2 in groups[g2]:
                        combined = self.combine_terms(term1, term2)
                        if combined:
                            next_groups.setdefault(g1, []).append(combined)
                            used.add(term1)
                            used.add(term2)

            checked |= unchecked - used
            unchecked = set(itertools.chain(*next_groups.values()))
            groups = next_groups

        prime_implicants |= checked
        return list(prime_implicants)

    def group_by_ones(self, terms):
        """
        Groups binary terms by the number of 1s in their representation.
        :param terms: A list of binary strings representing minterms.
        :return: A dictionary where the keys are the count of 1s, and values are lists of terms.
        """
        groups = {}
        for term in terms:
            count = term.count('1')
            groups.setdefault(count, []).append(term)
        return groups

    def combine_terms(self, term1, term2):
        """
        Combines two terms if they differ by exactly one bit, introducing a '-'.
        :param term1: The first binary term.
        :param term2: The second binary term.
        :return: A combined term or None if the terms differ by more than one bit.
        """
        combined = []
        found_difference = False

        for b1, b2 in zip(term1, term2):
            if b1 == b2:
                combined.append(b1)
            elif not found_difference:
                combined.append('-')
                found_difference = True
            else:
                return None  # More than one difference

        return ''.join(combined)

    def write_pla(self, filename, header, minterms):
        """
        Writes the minimized PLA file, preserving header information and appending minimized terms.
        :param filename: The path to the output PLA file.
        :param header: The header information from the original PLA file.
        :param minterms: The minimized terms (prime implicants).
        """
        with open(filename, 'w') as file:
            for line in header:
                if line.strip() != ".e":  # Skip .e to avoid duplication
                    file.write(line + "\n")
            for term in minterms:
                # Correctly replace '2' (if generated) with '-'
                formatted_term = term.replace('2', '-')  
                file.write(f"{formatted_term} 1\n")
            
            
            file.write(".e\n")


def main():
    """
    Main function to run the Quine-McCluskey algorithm on a given PLA file.
    Reads the input PLA file, minimizes it, and writes the minimized output to a new file.
    """
    input_file = "c:\\Users\\prime\\OneDrive\\Desktop\\C\\QM\\input8.pla"  
    output_file = "c:\\Users\\prime\\OneDrive\\Desktop\\C\\QM\\output8.pla"
 
    #Parse header to retain metadata
    #Adjust based on your PLA file
    num_vars = 4  
    
    qm = QuinMcAlgo(num_vars)
    header, minterms = qm.parse_pla(input_file)
    minimized = qm.minimize(minterms)
    qm.write_pla(output_file, header, minimized)

if __name__ == "__main__":
    
    main()

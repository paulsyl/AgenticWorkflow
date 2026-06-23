#!/usr/bin/env python3
import sys, os

def main():
    if len(sys.argv) < 2 or not os.path.exists(sys.argv[1]):
        sys.exit(1)
    
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        print(f.read())

if __name__ == "__main__": main()

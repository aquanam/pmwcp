from os import mkdir, getuid, system

if getuid() != 0:
    print("\33[1;49;91mPlease run as an administrator.\33[0m")
    exit(1)

print("\33[1;49;95mWelcome to the pmwcp setup!\33[0m")
print("\33[1;49;97mPlease wait, this could take a bit...\33[0m")

print("\33[1;49;92mCreating vital pmwcp directories...\33[0m")

for dirs in ["/var/lib/pmwcp",
             "/var/lib/pmwcp/unders",
             "/var/log/pmwcp",
             "/var/log/pmwcp/threads"]:
    print(f"\33[1;49;97m\t- {dirs}...\33[0m")

    try:
        mkdir(dirs)
    except FileExistsError:
        print(f"\33[1;49;93m\tHuh, directory '{dirs}' already exists.\33[0m")

print("\33[1;49;92mTouching vital pmwcp files...\33[0m")

for file in ["/var/lib/pmwcp/unders/favorites",
             "/var/lib/pmwcp/unders/whole",
             "/var/lib/pmwcp/installed_packages"]:
    print(f"\33[1;49;97m\t- {file}...\33[0m")
    
    system(f"sudo touch {file}")

print("\33[1;49;95mThe setup has now successfully finished!\33[0m")
print("\33[1;49;97mYou can now run pmwcp by running 'pmwcp' :)\33[0m")

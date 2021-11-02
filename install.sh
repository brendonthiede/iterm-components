#!/usr/bin/env bash

iterm_scripts_dir="${HOME}/Library/Application Support/iTerm2/Scripts"
autolaunch_dir="${iterm_scripts_dir}/AutoLaunch"

mkdir -p "${autolaunch_dir}"

echo "Copying scripts to AutoLaunch folder ${autolaunch_dir}"

for script in $(ls *.py); do
    echo "Copying ${script}..."
    rm -f "${autolaunch_dir}/${script}"
    cp "${script}" "${autolaunch_dir}/${script}"
    replacement_tokens="$(sed 's/\({{.*}}\)/\n\1\n/g' "${script}" | grep '{{.*}}')" || continue
    echo "  Replacing tokens..."
    for token in ${replacement_tokens}; do
        token_name="$(echo ${token} | sed 's/{{\(.*\)}}/\1/')"
        token_value="$(eval echo \$${token_name})"
        echo "    Replacing ${token_name} with ${token_value}"
        sed -i "s|{{${token_name}}}|${token_value}|g" "${autolaunch_dir}/${script}"
    done
done

#!/bin/bash

# Function to copy files from hexagonal directories
copy_hexagonal() {
  local max_i=0
  local max_j=0

  # Find maximum i and j for hexagonal
  for dir in ../hexagonal_2d_disabs/res_*_*; do
    if [[ $dir =~ res_([0-9]+)_([0-9]+) ]]; then
      if [[ "${BASH_REMATCH[1]}" -gt "$max_i" ]]; then
        max_i=${BASH_REMATCH[1]}
      fi
      if [[ "${BASH_REMATCH[2]}" -gt "$max_j" ]]; then
        max_j=${BASH_REMATCH[2]}
      fi
    fi
  done

  # Copy files for hexagonal
  for ((i=1; i<=max_i; i++)); do
    for ((j=1; j<=max_j; j++)); do
      src="../hexagonal_2d_disabs/res_${i}_${j}/average_surface_coverage.txt"
      dst="./hon_${i}_${j}_av_sur_coverage.txt"
      if [[ -f "$src" ]]; then
        cp "$src" "$dst"
        echo "Copied $src to $dst"
      else
        echo "Source file $src does not exist. Skipping."
      fi
    done
  done
}

# Function to copy files from triangular directories
copy_triangular() {
  local max_i=0
  local max_j=0

  # Find maximum i and j for triangular
  for dir in ../triangular_2d_disabs/res_*_*; do
    if [[ $dir =~ res_([0-9]+)_([0-9]+) ]]; then
      if [[ "${BASH_REMATCH[1]}" -gt "$max_i" ]]; then
        max_i=${BASH_REMATCH[1]}
      fi
      if [[ "${BASH_REMATCH[2]}" -gt "$max_j" ]]; then
        max_j=${BASH_REMATCH[2]}
      fi
    fi
  done

  # Copy files for triangular
  for ((i=1; i<=max_i; i++)); do
    for ((j=1; j<=max_j; j++)); do
      src="../triangular_2d_disabs/res_${i}_${j}/average_surface_coverage.txt"
      dst="./tri_${i}_${j}_av_sur_coverage.txt"
      if [[ -f "$src" ]]; then
        cp "$src" "$dst"
        echo "Copied $src to $dst"
      else
        echo "Source file $src does not exist. Skipping."
      fi
    done
  done
}

# Copy files from hexagonal directories
echo "Processing hexagonal directories..."
copy_hexagonal

# Copy files from triangular directories
echo "Processing triangular directories..."
copy_triangular


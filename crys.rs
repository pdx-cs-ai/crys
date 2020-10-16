/// Cryptarithm solver using DFS
/// Bart Massey

use std::collections::HashSet as Set;
use std::collections::HashMap as Map;
use std::io::*;

/// Dictionary type for keeping track of set variables.
type Env = Map<char, usize>;

/// Puzzle instance.
struct Puzzle {
    /// Terms.
    lines: [Vec<char>;3],
    /// Variables.
    pvars: Vec<char>,
    /// Columns.
    tuples: Vec<[char;3]>,
    /// Leading variables for terms.
    leading: Set<char>,
}
    
impl Puzzle {
    /// Read a puzzle instance.
    fn new<T:Read>(f: T) -> Self {

        // Read and split the next non-blank line.
        fn read_line<T>(f: &mut T) -> Vec<char>
            where T: Iterator<Item=Result<String>>
        {
            let mut line;
            loop {
                line = f
                    .next()
                    .expect("end of input on line read")
                    .expect("IO error reading line");
                if let Some(c) = line.trim().chars().next() {
                    if c != '#' {
                        break;
                    }
                }
            }
            line.trim().chars().collect()
        }

        // Read the instance description.
        let mut f = BufReader::new(f).lines();
        // XXX Rust arrays are garbage.
        let mut lines = [
            read_line(&mut f),
            read_line(&mut f),
            read_line(&mut f),
        ];

        // Normalize the line lengths by left-padding with "letter" 0.
        let max_width = lines.iter().map(|l| l.len()).max().unwrap();
        for l in &mut lines {
            // XXX Inefficient but doesn't matter here.
            for _ in 0..(max_width - l.len()) {
                l.insert(0, '0');
            }
        }

        // Order the variables right-to-left top-to-bottom.
        let mut pvars = Vec::new();
        let mut pvars_seen = Set::new();
        for j in (0..max_width).rev() {
            for line in &lines {
                let c = line[j];
                if c == '0' {
                    continue;
                }
                if pvars_seen.contains(&c) {
                    continue;
                }
                pvars.push(c);
                pvars_seen.insert(c);
            }
        }

        // List tuples forming the columns of the equation.
        let tuples = (0..max_width)
            .rev()
            .map(|i| [
                lines[0][i],
                lines[1][i],
                lines[2][i],
            ])
            .collect();
    
        // List of variables that lead the terms.
        let mut leading = Set::new();
        for line in lines.iter() {
            for &c in line {
                if c != '0' {
                    leading.insert(c);
                    break;
                }
            }
        }

        Self { lines, pvars, tuples, leading }
    }

    /// Print out a puzzle with solved variables substituted.
    fn show(&self, vals: Option<&Env>) {
        for l in &self.lines {
            for &c in l {
                if c == '0' {
                    print!(" ");
                    continue;
                }
                match vals {
                    None => print!("{}", c),
                    Some(e) => {
                        match e.get(&c) {
                            Some(d) => print!("{}", d),
                            None => print!("{}", c),
                        }
                    },
                }
            }
            println!();
        }
    }

    /// Return True iff no constraint violations
    fn ok(&self, vals: &Env) -> bool {
        // Return the value of the variable,
        // or None if unvalued.
        fn value(vals: &Env, var: char) -> Option<usize> {
            match var {
                '0' => Some(0),
                v => vals.get(&v).copied(),
            }
        }

        // Check for leading 0s.
        for &var in &self.leading {
            if let Some(0) = value(vals, var) {
                return false;
            }
        }

        // Check addition.
        let mut carry = 0;
        for t in &self.tuples {
            let v1 = value(vals, t[0]);
            let v2 = value(vals, t[1]);
            let vs = value(vals, t[2]);
            match (v1, v2, vs) {
                (Some(v1), Some(v2), Some(vs)) => {
                    let total = v1 + v2 + carry;
                    if total % 10 != vs {
                        return false;
                    }
                    carry = total / 10;
                },
                _ => return true,
            };
        }
        
        // Last carry-out should be 0.
        carry == 0
    }

    /// Solve a cryptarithm. *Strategy:* depth-first search
    /// with variables ordered right-to-left and lowest
    /// values tried first.
    fn solve(&self, pvars: &mut Vec<char>, vals: &mut Env) -> Option<Env> {
        // Base case: check for failure.
        if !self.ok(vals) {
            // println!("fail");
            // self.show(Some(vals));
            return None;
        }

        // Base case: check for solution.
        if pvars.is_empty() {
            // println!("succeed");
            // self.show(Some(vals));
            return Some(vals.to_owned());
        }

        // Recursive case: try to extend partial assignment.
        let used: Set<usize> = vals.values().copied().collect();
        let v = pvars.pop().unwrap();
        // println!("start {}", v);
        for val in 0..10 {
            if used.contains(&val) {
                continue;
            }
            vals.insert(v, val);
            let soln = self.solve(pvars, vals);
            if soln.is_some() {
                return soln;
            }
        }

        // No solution found. Undo the current assignment and
        // return failure.
        vals.remove(&v);
        pvars.push(v);
        None
    }

    /// Use the solver to solve a puzzle.
    fn solve_puzzle(&self) -> Option<Env> {
        let mut pvars = self.pvars.clone();
        let mut vals = Map::new();
        self.solve(&mut pvars, &mut vals)
    }
}

fn main() {
    let fname = std::env::args().nth(1).unwrap();
    let f = std::fs::File::open(fname).expect("could not open file");
    let puzzle = Puzzle::new(f);
    puzzle.show(None);
    println!();
    match puzzle.solve_puzzle() {
        None => println!("unsat"),
        Some(vals) => puzzle.show(Some(&vals)),
    }
}
